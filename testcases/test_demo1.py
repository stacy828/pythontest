import pytest
from test_placeholder_api import call_api
import responses
from urllib.parse import urljoin, urlencode, urlunparse, urlparse

base_url = "http://shop-xo.hctestedu.com/index.php?s="


def test_api_001():
    url = base_url + 'api/region/index'
    param = {"application": "web","application_client_type":"pc","token":"token","pid":0}
    response = call_api(url=url, method="POST",params=param)
    print(response.json())


#利用responses mock返回异常的response
@responses.activate
def test_api_negative_002():
    param = {"application": "web","application_client_type":"pc","token":"token","pid":0}
    query_string = urlencode(param)
    url = f"{base_url}?{query_string}"
    responses.add(
        responses.POST,
        url,
        json={"msg": "success","code": 0,"data": []},
        status=400
    )
    response = call_api(url=url, method="POST")
    assert response.status_code == 400
    print("第二个测试案例######################################")
    print(url)
    print(response.status_code)
    print(response.json())
