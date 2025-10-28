import os
import yaml


class yamlUtil:

    #读取yaml文件内容并返回
    def  read_extract_yaml(self, yaml_path):
        with open(os.getcwd() + yaml_path, mode='r', encoding="utf-8") as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value

    #将指定的数据写入yaml文件
    def write_extract_yaml(self,data):
        with open(os.getcwd()+"/extract.yaml", mode="a", encoding="utf-8") as f:
            yaml.dump(data=data,stream=f,allow_unicode=True)

    #清楚yaml文件
    def clear_extract_yaml(self,data):
        with open(os.getcwd()+"/extract.yaml",mode="w",encoding="utf-8") as f:
            f.truncate()

