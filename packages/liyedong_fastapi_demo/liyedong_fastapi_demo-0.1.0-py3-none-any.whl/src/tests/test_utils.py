
import os

from liyedong_fastapi_demo.utils import chdir


def test_chdir():
    path = 'D:\\Users\\Administrator\\Desktop\\python学习demo\\liyedong_fastapi_demo\\src\\tests'
    cwd = os.getcwd()
    with chdir(path):
        assert path == os.getcwd()
    assert cwd == os.getcwd()