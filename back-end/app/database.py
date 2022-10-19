import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser
from sqlalchemy_utils import create_database,database_exists


class MyConf(ConfigParser):
    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding='utf-8')


config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
conf = MyConf(config_path)
user = conf.get('mysql', 'user')
password = conf.get('mysql', 'password')
host = conf.get('mysql', 'host')
dbname = conf.get('mysql', 'dbname')


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}:3306/{}".format(user, password, host, dbname)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=True
)
if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
