import pytest
import allure
import allure_pytest


class test_api:
    @pytest.mark.parametrize('name,age',[['a','23'],['b','18'],['c','60']])
    def test_01(self, name, age):
        print("\n"+name, age)


if __name__ == '__main__':
    pytest.main(['test_api.py', '-sv'])

