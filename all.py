import os
import pytest

##用于执行测试案例
if __name__ == '__main__':
    pytest.main(["./testcases/", "-sv", "--alluredir", "./temps"])
    # os.system("allure generate ./temps -o ./report --clean")
