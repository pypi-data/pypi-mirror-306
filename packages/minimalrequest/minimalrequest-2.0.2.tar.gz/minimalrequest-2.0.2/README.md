# Introduction

`minimalrequest` is a analysis tool to determine the minimum valid API request data (including headers, query params, and payload) required to receive a valid response from an endpoint. It is designed to help in the process of reverse engineering complex third party API's and identifying the smallest, most efficient request that can be made.

# Installation

```
pip install minimalrequest
```

# Methodology

`minimalrequest` works by applying a simple algorithm to pare down requests.

1. An initial request is passed that might contain extra headers, query params, or JSON payload data that doesn't effect the value of the JSON response received. A request to that endpoint is made and the response is saved as the "reference" response.
2. Each request element (this could be a header, query param, or JSON payload property) is removed and a test request is sent.
3. If the test request suceeds, the test response is compared to the reference response using one of several equivalency modes.
4. If the test response is deemed equivalent to the reference response, the request element is removed.

# Usage

All functionality is exposed through the `minimal_request_finder` function.

```py
from minimalrequest import minimal_request_finder
```

Initial requests can be passed as a curl command:

```py
result = minimal_request_finder(
    curl="""
        curl -XPOST -H 'header-one: one' -H 'header-two: two' -H 'header-three: three' -H "Content-Type: application/json" -d '{
            "property1": {"subproperty1": "one", "subproperty2": "two"},
            "property2": [1, 2, 3, 4, 5]
        }' 'https://api.com/endpoint/v1/test?param1=1&param2=2&param3=3'
    """
)
```

or can be passed as individual arguments:

```py
result = minimal_request_finder(
    http_method="post",
    url="https://api.com/endpoint/v1/test",
    query_params={"param1": "value", "param2": "value"},
    headers={"Content-Type": "application/json"},
    payload={"requestData": {"query": "test", "pages": 2}}
)
```

Results are returned as a `MinimalRequestResult` which contains the `url` and minimal `query_params`, `headers`, and `payload`.

# Equivalency Modes

The `minimal_request_finder` function accepts an `equivalency_mode` argument to change the method used to check equivalency between the reference response and test responses.

## Exact Equivalency

Setting the `equivalency_mode` to `exact` (it's default value) will only consider the test response and reference to be equivalent when their parsed Python object representations are exactly the same (`==`). This mode is intended for API's with a completely deterministic output based on each input.

## Types Equivalency

The `types` equivalency mode compares each response object property or array element for data *type* equivalency rather than exact values. This mode can be useful any time an API response should have constant data structure, but some amount of variable or random content, such as a timestamp or hash value.

The `types` mode works with the `types_check_exact_list_equivalency` flag (defaults to `True`). If set to `False`, the equivalency check allows the number of elements in arrays throughout the response to vary in length between the test and reference response as long as any existing array elements pass the type check. This flag can be useful if your API response contains arrays of variable or random length, such as events over a given time period.

## Size Equivalency

For highly variable API responses that might not work with other modes, the `size` equivalency mode can be used. This check converts the reference and test responses into JSON string representations and passes equivalency if the test response size in bytes is within some percent tolerance of the reference response size. The `size_equivalency_tolerance` argument (default value of 0.05) sets this tolerance value.