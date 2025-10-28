import pytest
import os
import requests

from common import yaml_util


class test_get:
    #方法一：直接将要参数化的数据写在parametrize后面
    @pytest.mark.parametrize("qqid",[2586168620,599928887,123456783])
    def test_get_qqname(self,qqid):
        url = "https://api.oioweb.cn/api/qq/nickname"
        data = {"qq":qqid}
        res = requests.request(method="get", url=url, params=data)
        res_code = res.json()['code']
        print(res.json())
        print(res.json()['code'])

    #方法二 将数据放在一个yaml文件里，通过yaml_util.py里的方法去读取，然后再参数化
    @pytest.mark.parametrize("qqlist",yaml_util.yamlUtil().read_extract_yaml(yaml_path="/data/test_get.yaml"))
    def test_get_qqname2(self,qqlist):
        url = "https://api.oioweb.cn/api/qq/nickname"
        qqid = qqlist['qqid']
        data = {"qq":qqid}
        res = requests.request(method="get", url=url, params=data)
        res_code = res.json()['code']
        print(res.json())
        print(res.json()['code'])


