import pytest
import requests
import allure
from xToolkit import xfile
import json,jsonpath
from string import Template

#class名字以Test开头
class Test_request:

    #定义一个空字典，用于存储登录的token值
    dict = {}

    #数据驱动，读取excel里的案例数据，工作表从0开始，sheet1为0
    test_data = xfile.read("D:\\模拟接口测试用例.xls").excel_to_dict(sheet=0)
    print(test_data)

    #pytest装饰器，修饰函数，循环次数由列表长度决定，自动解析列表
    #函数以test开头才能识别到
    @pytest.mark.parametrize("test_info",test_data)
    def test_execute_api(self,test_info):
        url = test_info['接口URL']
        #处理带关联的参数
        if "$" in url:
            Template(url).subsititue(dict)

        rs = requests.request(url=test_info['接口URL'],
                              method=test_info['请求方式'],
                              params=eval(test_info['URL参数']),
                              data=eval(test_info['body参数']))

        print(rs.json())
        print( rs.json()['code'])
        # rs_code = rs.json()['code']
        # assert rs_code == 0

        # 获取登录接口response中的token
        # test_info['提取参数']=token
        if test_info['提取参数']:
            val = jsonpath.jsonpath(rs.json(),"$.."+test_info['提取参数'])
            dict[test_info['提取参数']] = val[0]

    #执行主函数
    if __name__ == '__main__':
        pytest.main(['test_api_auto.py', '-sv'])





