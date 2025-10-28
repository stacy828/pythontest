import requests
import pytest
from typing import Optional, Dict, Any, Union

host_url = "https://jsonplaceholder.typicode.com"

"""
   通用的API调用方法

   Args:
       url: 请求的URL
       method: HTTP方法 (GET, POST, PUT, DELETE, etc.)
       params: URL参数 (用于GET请求)
       data: 请求体数据 (表单数据)
       json: JSON格式的请求体数据
       headers: 请求头
       timeout: 超时时间
       **kwargs: 其他requests参数

   Returns:
       requests.Response对象
   """


def call_api(
    url: str,
    method: str = 'GET',
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Union[Dict[str, Any], str]] = None,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    **kwargs
) -> requests.Response:

    method = method.upper() #将method值转为大写
    try:
        response = requests.request(method=method,
                                    url=url,
                                    params=params,
                                    data=data,
                                    json=json,
                                    headers=headers,
                                    timeout=timeout,
                                    **kwargs)
        print(response.json())
        response.raise_for_status() #在http错误时抛出异常
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败：{str(e)}")
        print(e)


class Test_api:

    def test_get_request(self):
        url=host_url +'/posts/1'
        response = call_api(url=url,method='GET')
        assert response.status_code == 200
        assert response.json()['userId'] == 1
        assert response.json()['id'] == 1
        assert 'title' in response.json()

    def test_get_request_with_param(self):
        url=host_url +'/posts/1'
        param = {'id': 1}
        response = call_api(url=url,method='GET',params=param)
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_post_request(self):
        url=host_url +'/posts'
        json = {
            'title': 'foo',
            'body': 'bar',
            'userId': 1
        }
        header = {'Content-type': 'application/json; charset=UTF-8'}
        response = call_api(url=url, method='POST', json=json, headers=header)
        assert response.status_code == 201
        assert len(response.json()) > 0
        assert response.json()['id'] == 101

    def test_error_handling(self):
        """测试错误处理"""
        with pytest.raises(Exception) as exc_info:
            # 测试无效URL
            call_api("http://invalid-url-that-does-not-exist.com9/", "GET")
            print(exc_info.value)
            assert "API调用失败" in str(exc_info.value)

        with pytest.raises(Exception) as exc_info:
            result = call_api("http://httpbin.org/status/404", "GET")
            print("111111111111")
            print(f"状态码: {result.status_code}")  # 使用f-string更清晰
            assert result.status_code == 404


    def test_error_handling_debug(self):
        """调试错误处理"""
        try:
            result = call_api("http://invalid-url-that-does-not-exist.com", "GET")
            print(f"意外成功，返回结果: {result}")
            assert False, "预期抛出异常但函数成功返回"
        except Exception as e:
            print(f"正确抛出异常: {type(e).__name__}: {e}")


    def test_timeout(self):
        """测试超时处理"""
        with pytest.raises(Exception) as exc_info:
            # 测试超时（设置极短的超时时间）
            call_api(f"{host_url}/delay/2", "GET", timeout=0.001)
        print(exc_info)
        #严重返回的exception里有time out
        assert "timeout" in str(exc_info.value).lower() or "timed out" in str(exc_info.value).lower()




# 执行主函数
if __name__ == '__main__':
    pytest.main(['test_placeholder_api.py', '-sv'])
