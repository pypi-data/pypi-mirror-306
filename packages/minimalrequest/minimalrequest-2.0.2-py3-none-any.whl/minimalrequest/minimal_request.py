import asyncio
import json
import sys
from copy import copy, deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Coroutine, Literal, Sequence, cast
from urllib import parse

import curlparser
from httpx import AsyncClient

from minimalrequest.rate_limiter import RateLimiter

HttpMethod = Literal["get", "post"]
QueryParams = dict[str, Any]
Headers = dict[str, Any]
Payload = dict[str, Any]
JsonObject = dict[str, Any] | list[Any]
EquivalencyMode = Literal["exact", "types", "size"]


@dataclass
class MinimalRequestResult:
    url: str
    query_params: QueryParams | None
    headers: Headers | None
    payload: JsonObject | None


def minimal_request_finder(
    curl: str | None = None,
    http_method: HttpMethod | None = None,
    url: str | None = None,
    query_params: QueryParams | None = None,
    headers: Headers | None = None,
    payload: Payload | None = None,
    equivalency_mode: EquivalencyMode = "exact",
    size_equivalency_tolerance: float = 0.05,
    types_check_exact_list_equivalency=True,
    requests_per_second_limit: float = 0,
    output_file_path: str | None = None,
):
    """Determines the minimum required API request (including query params, headers, and payload)
    required to receive a correct response from some endpoint. Works by removing elements from the
    request, sending a test request, and comparing the test response to a reference response. If
    the test response matches the reference response via the selected equivalency mode, that element
    is removed as non-essential to the output.

    Args:
        curl (str | None, optional): A curl command for the desired request that can be provided
            instead of the `http_method`, `url`, `query_params`, `headers`, and `payload` arguments.
            Defaults to None.
        http_method (HttpMethod | None, optional): The HTTP method to use for the request. Defaults to None.
        url (str | None, optional): The base URL of the request. Defaults to None.
        query_params (QueryParams | None, optional): A dictionary of query param values for the request.
            Defaults to None.
        headers (Headers | None, optional): A dictionary of headers for the request. Defaults to None.
        payload (JsonObject | None, optional): The JSON payload for the request. Defaults to None.
        equivalency_mode (EquivalencyMode, optional): The method to use to determine whether the test
            responses match the correct reference response. The "size" option checks that the size in
            bytes of the test response is within an allowed tolerance of the size of the reference
            response. This is the loosest check and is ideal when the desired response is large,
            complex, or random. The "types" option performs a property by property comparison from the
            reference response to the test response and passes if the property types match. This option
            can be used for responses with varying content but consistent object structure. The "exact"
            option is the most restrictive and checks that the test response is an exact match of the
            reference response. Defaults to "exact".
        size_equivalency_tolerance (float, optional): The tolerance percentage from 0 to 1 in size
            variance that a test response is allowed to have from the reference response and still
            be considered equivalent. This argument is only used when the `equivalency_mode` is set
            to "size" and is ignored otherwise. Defaults to 0.05.
        types_check_exact_list_equivalency (bool, optional): Enforces list (i.e. JSON array) index
            equivalency between lists in the test response versus the reference response when checking
            with "types" equivalency mode. When set to `True`, lists are compared element by
            element and elements missing from the test response will cause the test to fail equivalency.
            Setting to `False` ignores any list elements missing from the test response. Setting to `False`
            can be useful if the response to test might contain an array with a variable number of items.
            This argument is used only when the `equivalency_mode` is set to "types" and is ignored otherwise.
            Defaults to True.
        requests_per_second_limit (float, optional): The max rate limit allowed for test requests. Can be
            used if the API you are testing against is rate limited. Defaults to 0 which allows an unlimited
            effective rate limit.
        output_file_path (str | None, optional): Outputs the minimum request elements (query params,
            headers, and payload) to a JSON file at the path specified. If not set, no output file is created.
            Defaults to None.

    Raises:
        ValueError: _description_

    Returns:
        MinimumRequestResult: A result class containing the minimum request elements.
    """

    if curl:
        http_method, url, query_params, headers, payload = _parse_curl(curl)

        if not http_method or not url:
            raise ValueError(
                "Invalid cURL command. Unable to extract a valid URL and HTTP method."
            )
    elif not http_method or not url:
        raise ValueError(
            "A value for either the `curl` argument or the `http_method` and `url` arguments "
            "must be provided."
        )

    return asyncio.run(
        _run(
            http_method,
            url,
            deepcopy(query_params),
            copy(headers),
            deepcopy(payload),
            equivalency_mode,
            size_equivalency_tolerance,
            types_check_exact_list_equivalency,
            requests_per_second_limit,
            output_file_path,
        )
    )


@dataclass
class _RequestResult:
    status: int
    text: str


class _WorkerResult:
    def __init__(self, request_element: str | int):
        self.request_element = request_element
        self.remove = False


def _parse_curl(curl: str):
    parsed_command = curlparser.parse(curl)

    http_method = cast(HttpMethod, parsed_command.method.lower())

    url_with_query_params = cast(str, parsed_command.url)
    query_string = parse.urlparse(url_with_query_params).query
    url = url_with_query_params.replace(f"?{query_string}", "")

    query_params: QueryParams = {
        param: value[0] for param, value in parse.parse_qs(query_string).items()
    }
    headers = cast(Headers, {**parsed_command.header, **parsed_command.cookies})
    payload = cast(dict[str, Any], parsed_command.json)

    for key, value in headers.items():
        headers[key] = str(value).strip()

    # Clean up extra content-type header values since the curlparser determines this automatically
    content_type_keys = {key for key in headers.keys() if key.lower() == "content-type"}

    if len(content_type_keys) >= 2:
        for content_type_key in content_type_keys:
            if content_type_key != "Content-Type":
                del headers[key]

    return http_method, url, query_params, headers, payload


def _get_accessors(object: JsonObject):
    if isinstance(object, dict):
        return object.keys()
    else:
        # Return in reverse order for safe deletion of list elements
        return (i for i in reversed(range(0, len(object))))


def _get_object_value_by_path(
    object: QueryParams | Headers | JsonObject, path: Sequence
):
    value: JsonObject = object

    for element in path:
        value = value[element]

    return value


def _delete_object_value_by_path(
    object: QueryParams | Headers | JsonObject, path: Sequence[Any]
):
    value = object

    for i, element in enumerate(path):
        if i == len(path) - 1:
            del value[element]
        else:
            value = value[element]


def _get_query_params_test_function(
    client: AsyncClient,
    http_method: HttpMethod,
    url: str,
    headers: Headers | None,
    payload: Payload | None,
):
    def _send_test_request(query_params: QueryParams):
        url_with_query_params = f"{url}?{parse.urlencode(query_params)}"

        return _send_request(
            client, http_method, url_with_query_params, headers, payload
        )

    return _send_test_request


def _get_headers_test_function(
    client: AsyncClient,
    http_method: HttpMethod,
    url_with_query_params: str,
    payload: Payload | None,
):
    def _send_test_request(headers: Headers):
        return _send_request(
            client, http_method, url_with_query_params, headers, payload
        )

    return _send_test_request


def _get_payload_test_function(
    client: AsyncClient,
    http_method: HttpMethod,
    url_with_query_params: str,
    headers: Headers | None,
):
    def _send_test_request(payload: Payload):
        return _send_request(
            client, http_method, url_with_query_params, headers, payload
        )

    return _send_test_request


def _check_type_equivalency(
    reference_response: Payload,
    test_response: Payload,
    path: Sequence[Any],
    types_check_exact_list_equivalency: bool,
) -> bool:
    for accessor in _get_accessors(_get_object_value_by_path(reference_response, path)):
        try:
            reference_value = _get_object_value_by_path(
                reference_response, [*path, accessor]
            )
            test_value = _get_object_value_by_path(test_response, [*path, accessor])

            if type(reference_value) != type(test_value):
                return False
        except KeyError:
            return False
        except IndexError:
            if types_check_exact_list_equivalency:
                return False
            else:
                return True

        if isinstance(reference_value, (dict, list)):
            return _check_type_equivalency(
                reference_response,
                test_response,
                [*path, accessor],
                types_check_exact_list_equivalency,
            )

    return True


async def _run(
    http_method: HttpMethod,
    url: str,
    query_params: QueryParams | None,
    headers: Headers | None,
    payload: Payload | None,
    equivalency_mode: EquivalencyMode,
    size_equivalency_tolerance: float,
    types_check_exact_list_equivalency: bool,
    requests_per_second_limit: float,
    output_file_path: str | None,
):
    url_with_query_params = (
        f"{url}?{parse.urlencode(query_params)}" if query_params else url
    )

    async with AsyncClient() as client:
        response = await _send_request(
            client, http_method, url_with_query_params, headers, payload
        )

        if response.status >= 400:
            raise RuntimeError(
                "Received an error response on the initial API request.\n\n"
                f"{response.status} - {response.text}\n\n"
                "Check that the `url`, `query_params`, `headers`, and `payload` arguments are correct."
            )

        reference_response: Payload = json.loads(response.text)

        if query_params:
            _send_test_request = _get_query_params_test_function(
                client, http_method, url, headers, payload
            )

            await _process_request_element_group(
                [],
                query_params,
                _send_test_request,
                reference_response,
                equivalency_mode,
                size_equivalency_tolerance,
                types_check_exact_list_equivalency,
                requests_per_second_limit,
            )

        if headers:
            _send_test_request = _get_headers_test_function(
                client, http_method, url_with_query_params, payload
            )

            await _process_request_element_group(
                [],
                headers,
                _send_test_request,
                reference_response,
                equivalency_mode,
                size_equivalency_tolerance,
                types_check_exact_list_equivalency,
                requests_per_second_limit,
            )

        if payload:
            _send_test_request = _get_payload_test_function(
                client, http_method, url_with_query_params, headers
            )

            await _process_request_element_group(
                [],
                payload,
                _send_test_request,
                reference_response,
                equivalency_mode,
                size_equivalency_tolerance,
                types_check_exact_list_equivalency,
                requests_per_second_limit,
            )

        if output_file_path:
            output_json = {
                "url": url,
                "queryParams": query_params,
                "headers": headers,
                "payload": payload,
            }

            with open(output_file_path, "w") as output_file:
                output_file.write(json.dumps(output_json, indent=2))

            print(f"\nOutput file saved to {output_file_path}")

        return MinimalRequestResult(url, query_params, headers, payload)


async def _process_request_element_group[
    T: QueryParams | Headers | JsonObject
](
    path: Sequence[Any],
    request_element_group: T,
    send_test_request: Callable[[T], Coroutine[Any, Any, _RequestResult]],
    reference_response: Payload,
    equivalency_mode: EquivalencyMode,
    size_equivalency_tolerance: float,
    types_check_exact_list_equivalency: bool,
    requests_per_second_limit: float,
):
    requests_per_second_limit = (
        100000 if requests_per_second_limit == 0 else requests_per_second_limit
    )
    rate_limiter = RateLimiter(requests_per_second_limit, 1)
    tasks = tuple(
        asyncio.create_task(
            _request_element_worker(
                rate_limiter,
                [*path, accessor],
                request_element_group,
                send_test_request,
                reference_response,
                equivalency_mode,
                size_equivalency_tolerance,
                types_check_exact_list_equivalency,
            )
        )
        for accessor in _get_accessors(
            _get_object_value_by_path(request_element_group, path)
        )
    )

    results: list[_WorkerResult] = await asyncio.gather(*tasks)

    for result in results:
        if result.remove:
            _delete_object_value_by_path(
                request_element_group, [*path, result.request_element]
            )

    for accessor in _get_accessors(
        _get_object_value_by_path(request_element_group, path)
    ):
        if isinstance(
            _get_object_value_by_path(request_element_group, [*path, accessor]),
            (dict, list),
        ):
            await _process_request_element_group(
                [*path, accessor],
                request_element_group,
                send_test_request,
                reference_response,
                equivalency_mode,
                size_equivalency_tolerance,
                types_check_exact_list_equivalency,
                requests_per_second_limit,
            )


async def _request_element_worker[
    T: QueryParams | Headers | JsonObject
](
    rate_limiter: RateLimiter,
    path_to_request_element_to_test: Sequence[Any],
    request_element_group: T,
    send_test_request: Callable[[T], Coroutine[Any, Any, _RequestResult]],
    reference_response: Payload,
    equivalency_mode: EquivalencyMode,
    size_equivalency_tolerance: float,
    types_check_exact_list_equivalency: bool,
):
    request_element_to_test = path_to_request_element_to_test[-1]
    result = _WorkerResult(request_element_to_test)

    request_element_group_copy = deepcopy(request_element_group)
    _delete_object_value_by_path(
        request_element_group_copy, path_to_request_element_to_test
    )

    async with rate_limiter:
        response = await send_test_request(request_element_group_copy)

    if response.status >= 400:
        return result

    test_response = json.loads(response.text)

    if equivalency_mode == "exact" and reference_response == test_response:
        result.remove = True
    elif equivalency_mode == "types" and _check_type_equivalency(
        reference_response, test_response, [], types_check_exact_list_equivalency
    ):
        result.remove = True
    elif equivalency_mode == "size":
        reference_response_size = sys.getsizeof(json.dumps(reference_response))
        tolerance = reference_response_size * size_equivalency_tolerance
        test_response_size = sys.getsizeof(json.dumps(test_response))

        result.remove = (
            reference_response_size - tolerance
            <= test_response_size
            <= reference_response_size + tolerance
        )

    return result


async def _send_request(
    client: AsyncClient,
    http_method: HttpMethod,
    url: str,
    headers: Headers | None,
    payload: Payload | None,
):
    if headers:
        for key, value in headers.items():
            headers[key] = str(value)

    if http_method == "get":
        response = await client.get(url=url, headers=headers)
    else:
        response = await client.post(url=url, headers=headers, data=payload)

    return _RequestResult(response.status_code, response.text)
