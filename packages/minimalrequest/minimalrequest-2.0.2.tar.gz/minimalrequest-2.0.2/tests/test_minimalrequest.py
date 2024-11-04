import json
from copy import deepcopy
from typing import Any, cast
from unittest.mock import MagicMock
from urllib import parse

import httpx
import pytest

from minimalrequest import minimal_request_finder

curl = """
curl -XPOST -H 'header-one: one' -H 'header-two: two' -H 'header-three: three' -H "Content-Type: application/json" -d '{
    "property1": {"subproperty1": "one", "subproperty2": "two"},
    "property2": [1, 2, 3, 4, 5]
}' 'https://mock.api.com/endpoint/v1/test?param1=1&param2=2&param3=3'
"""

url = "https://mock.api.com/endpoint/v1/test"
initial_query_params = {"param1": 1, "param2": 2, "param3": 3}
initial_headers = {"header-one": "one", "header-two": "two", "header-three": "three"}
initial_payload = {
    "property1": {"subproperty1": "one", "subproperty2": "two"},
    "property2": [1, 2, 3, 4, 5],
}


mock_return_data = {
    "result": {
        "array": [1, 2, 3, 4, 5, 6],
        "object": {"property1": 1, "property2": "two", "property3": True},
    }
}


class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code


def mock_api_implementation(url: str, headers: dict[str, str], data: dict[str, Any]):
    mock_return_data_copy = deepcopy(mock_return_data)
    query_params = parse.parse_qs(parse.urlparse(url).query)

    if "param1" not in query_params:
        mock_return_data_copy["result"]["array"] = [1, 2, 3]

    if "param2" not in query_params:
        return MockResponse("{}", 200)

    if "header-one" not in headers:
        return MockResponse("{}", 400)

    if "property1" not in data:
        return MockResponse("{}", 200)

    if "subproperty2" not in data["property1"]:
        return MockResponse("{}", 200)

    if "property2" not in data:
        mock_return_data_copy["result"]["object"]["property3"] = False

    return MockResponse(json.dumps(mock_return_data_copy), 200)


@pytest.fixture
def mock_api(mocker):
    mocker.patch("httpx.AsyncClient.post")
    post_mock = cast(MagicMock, httpx.AsyncClient().post)
    post_mock.side_effect = mock_api_implementation


@pytest.mark.asyncio
def test_finds_minimum_request_from_curl_with_exact_equivalency_checks(mock_api):
    result = minimal_request_finder(curl=curl, equivalency_mode="exact")

    assert result.url == url
    assert result.query_params == {"param1": "1", "param2": "2"}
    assert result.headers == {"header-one": "one"}
    assert result.payload == {"property1": {"subproperty2": "two"}, "property2": []}


@pytest.mark.asyncio
def test_finds_minimum_request_with_exact_equivalency_checks(mock_api):
    result = minimal_request_finder(
        http_method="post",
        url=url,
        query_params=initial_query_params,
        headers=initial_headers,
        payload=initial_payload,
        equivalency_mode="exact",
    )

    assert result.url == url
    assert result.query_params == {"param1": 1, "param2": 2}
    assert result.headers == {"header-one": "one"}
    assert result.payload == {"property1": {"subproperty2": "two"}, "property2": []}


@pytest.mark.asyncio
def test_finds_minimum_request_with_types_equivalency_checks(mock_api):
    result = minimal_request_finder(
        http_method="post",
        url=url,
        query_params=initial_query_params,
        headers=initial_headers,
        payload=initial_payload,
        equivalency_mode="types",
    )

    assert result.url == url
    assert result.query_params == {"param1": 1, "param2": 2}
    assert result.headers == {"header-one": "one"}
    # property2 should be omitted because the returned False (versus the original True)
    # value passes the bool type check
    assert result.payload == {"property1": {"subproperty2": "two"}}


@pytest.mark.asyncio
def test_finds_minimum_request_with_types_equivalency_checks_and_list_inequivalency_tolerance(
    mock_api,
):
    result = minimal_request_finder(
        http_method="post",
        url=url,
        query_params=initial_query_params,
        headers=initial_headers,
        payload=initial_payload,
        equivalency_mode="types",
        types_check_exact_list_equivalency=False,
    )

    assert result.url == url
    # param1 should be omitted because list size inequivalency is allowed
    assert result.query_params == {"param2": 2}
    assert result.headers == {"header-one": "one"}
    # property2 should be omitted because the returned False (versus the original True)
    # value passes the bool type check
    assert result.payload == {"property1": {"subproperty2": "two"}}


@pytest.mark.asyncio
def test_finds_minimum_request_with_size_equivalency_checks(mock_api):
    result = minimal_request_finder(
        http_method="post",
        url=url,
        query_params=initial_query_params,
        headers=initial_headers,
        payload=initial_payload,
        equivalency_mode="size",
        size_equivalency_tolerance=0,
    )

    assert result.url == url
    assert result.query_params == {"param1": 1, "param2": 2}
    assert result.headers == {"header-one": "one"}
    assert result.payload == {"property1": {"subproperty2": "two"}, "property2": []}
