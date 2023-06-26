from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://pulsemonitoring:Jpxt280996%401406@192.168.50.251:3306/pulsemonitoring"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

Base = declarative_base()

def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = db()
    try:
        yield session
    finally:
        session.close()
