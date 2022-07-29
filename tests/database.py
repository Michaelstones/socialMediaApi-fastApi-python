from msilib import schema
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db,Base
import pytest





SQL_DATABASE_ALCHEMY_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


engine = create_engine(SQL_DATABASE_ALCHEMY_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session ():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()
    try:
            yield db
    finally:
            db.close()

    
@pytest.fixture()
def client (session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    
    
