# coding=utf-8
import os
import pytest
import allure


@allure.epic("epic名称")
@allure.feature("feature名称")
class TestClass1:

    def test_case_01(self):
        with allure.step("测试案例1的步骤"):
            token = '12345678a'
            print(token)

    @pytest.mark.usefixtures('setup')
    def test_case_02(self):
        token = '12345678b'
        print(token)

    @allure.step("测试案例3的步骤")
    def test_case_03(self):
        print("\n测试案例3")

    @allure.story("Story名称")
    def test_case_04(self):
        print("\n测试案例4")

    @allure.severity("critical")
    @allure.title("测试案例5标题")
    @allure.story("story5名称")
    @allure.issue("bug-1")
    @allure.testcase("测试案例5")
    def test_case_05(self):
        print("\n测试案例5")
