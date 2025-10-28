import pytest
import requests
from unittest.mock import patch, MagicMock
from test_placeholder_api import call_api  # 替换为实际模块名


class TestCallApi:

    @pytest.mark.parametrize("status_code, expected_exception_msg", [
        (400, "API调用失败：400 Client Error"),
        (401, "API调用失败：401 Client Error"),
        (403, "API调用失败：403 Client Error"),
        (404, "API调用失败：404 Client Error"),
        (500, "API调用失败：500 Server Error"),
        (502, "API调用失败：502 Server Error"),
        (503, "API调用失败：503 Server Error"),
    ])
    def test_call_api_with_error_status_codes(self, status_code, expected_exception_msg):
        """测试各种HTTP错误状态码"""
        # Mock响应对象
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            f"{status_code} Client Error" if 400 <= status_code < 500 else f"{status_code} Server Error"
        )

        # Mock requests.request方法
        with patch('test_placeholder_api.requests.request') as mock_request:
            mock_request.return_value = mock_response

            # 验证是否抛出异常
            with pytest.raises(Exception) as exc_info:
                call_api("https://api.example.com/test")

            # 验证异常消息
            assert expected_exception_msg in str(exc_info.value)

    def test_call_api_with_connection_error(self):
        """测试连接错误"""
        with patch('test_placeholder_api.requests.request') as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError("连接失败")

            with pytest.raises(Exception) as exc_info:
                call_api("https://jsonplaceholder.typicode.com/posts/1")

            print("\n")
            print(exc_info.value)
            assert "API调用失败：连接失败" in str(exc_info.value)

    def test_call_api_with_timeout_error(self):
        """测试超时错误"""
        with patch('test_placeholder_api.requests.request') as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout("请求超时")

            with pytest.raises(Exception) as exc_info:
                call_api("https://jsonplaceholder.typicode.com/posts/1", timeout=5)

            print("\n")
            print(exc_info.value)
            assert "API调用失败：请求超时" in str(exc_info.value)

    def test_call_api_with_request_exception(self):
        """测试其他请求异常"""
        with patch('test_placeholder_api.requests.request') as mock_request:
            mock_request.side_effect = requests.exceptions.RequestException("未知请求错误")

            with pytest.raises(Exception) as exc_info:
                call_api("https://jsonplaceholder.typicode.com/posts/1")

            print("\n")
            print(exc_info.value)
            assert "API调用失败：未知请求错误" in str(exc_info.value)

    def test_call_api_success(self):
        """测试成功调用"""
        # Mock成功的响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "success"}

        with patch('test_placeholder_api.requests.request') as mock_request:
            mock_request.return_value = mock_response

            response = call_api("https://jsonplaceholder.typicode.com/posts/1")

            print("响应结果：")
            # 验证返回的响应对象
            assert response == mock_response
            # 验证打印了响应JSON
            mock_response.json.assert_called_once()

    def test_call_api_with_different_methods(self):
        """测试不同HTTP方法"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

        with patch('test_placeholder_api.requests.request') as mock_request:
            mock_request.return_value = mock_response

            # 测试POST方法
            with pytest.raises(Exception):
                call_api("https://api.example.com/test", method="POST")
            mock_request.assert_called_with(
                method="POST",
                url="https://api.example.com/test",
                params=None,
                data=None,
                json=None,
                headers=None,
                timeout=30
            )

            # 测试PUT方法
            with pytest.raises(Exception):
                call_api("https://api.example.com/test", method="PUT", json={"key": "value"})
            mock_request.assert_called_with(
                method="PUT",
                url="https://api.example.com/test",
                params=None,
                data=None,
                json={"key": "value"},
                headers=None,
                timeout=30
            )

    def test_call_api_with_parameters(self):
        """测试带参数的调用"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Client Error")

        with patch('test_placeholder_api.requests.request') as mock_request:
            mock_request.return_value = mock_response

            test_params = {"page": 1, "limit": 10}
            test_headers = {"Authorization": "Bearer token"}

            with pytest.raises(Exception):
                call_api(
                    "https://api.example.com/test",
                    params=test_params,
                    headers=test_headers,
                    timeout=60
                )

            # 验证参数正确传递
            mock_request.assert_called_with(
                method="GET",
                url="https://api.example.com/test",
                params=test_params,
                data=None,
                json=None,
                headers=test_headers,
                timeout=60
            )