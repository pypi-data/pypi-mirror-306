import os

from liyedong_fastapi_demo.config import settings

settings.load_file(os.path.join(os.path.dirname(__file__), 'settings.yml'))
settings.load_file(os.path.join(os.path.dirname(__file__), 'settings.local.yml'))