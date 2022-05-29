from dotenv import load_dotenv
from operator import itemgetter
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

host, database, user, password = itemgetter(
    'host', 'database', 'user', 'password')(environ)
base_config = {
    'poolname': 'pulse-monitoring-app',
    'pool_size': 3
}

SQLALCHEMY_DATABASE_URL = f'jdbc:mysql://{user}:{password}@{host}:3306/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = automap_base()
