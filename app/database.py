from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from .config import settings


SQL_DATABASE_ALCHEMY_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQL_DATABASE_ALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


    
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres', password='mickshow', cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         print('connected successful')
#         break
#     except Exception as error:
#         print('connection failed')
#         print('Error', error)
#         time.sleep(2)