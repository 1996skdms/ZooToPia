from os import environ, path

from pydantic.dataclasses import dataclass

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@j5a602.p.ssafy.io:3306/bigdata?charset=utf8"

@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DEBUG: bool = False
    TEST_MODE: bool = False
    DB_URL: str = environ.get("DB_URL", SQLALCHEMY_DATABASE_URL)

def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(local=Config)
    return config[environ.get("API_ENV", "local")]()


