#!D:\Users\Administrator\Desktop\python学习demo\liyedong_fastapi_demo\venv\Scripts\python.exe
import sys

from liyedong_fastapi_demo.cmdline import main, server
from liyedong_fastapi_demo.db import engine
from liyedong_fastapi_demo.models import BaseModel


def init_db():
    BaseModel.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
    sys.exit(server())
