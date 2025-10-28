import pytest
import selenium

#该文件用于定义一些前置后置方法
@pytest.fixture(scope='function')
def setup():
    print("\n测试前置步骤开始")
    yield
    print("\n测试前置步骤关闭")


@pytest.fixture()
def teardown():
    print("\n测试后置步骤开始")
    yield
    print("\n测试后置步骤关闭")
