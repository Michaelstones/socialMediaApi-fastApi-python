from pyexpat import model
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import get_db,Base
from app.oauth import create_Jwt_Token
import pytest
from app import schema, models
from jose import jwt





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
    
    
    
@pytest.fixture
def test_user_d (client):
    user_data ={
        'email':'mick@gmail.com',
        'password':'mickshow'
    }
    res = client.post('/users/', json=user_data)
    assert res.status_code ==201
    new_user = res.json()
    new_user['password'] = user_data['password']
    
    return new_user
    
@pytest.fixture
def test_user_create(client):
    res = client.post('/users/', json={'email':'mick@gmail.com', 'password':'mickshow'})
    new_user=schema.UserRespon(**res.json())
    assert new_user.email== 'mick@gmail.com'
    assert res.status_code==201


@pytest.fixture
def test_user_login(client, test_user_d):
    res = client.post('/login', data={'username':test_user_d['email'], 'password':test_user_d['password']})
    login_validate = schema.Token(**res.json())
    check = jwt.decode(login_validate.access_Token, settings.secret_key, settings.algorithm)
    id:str = check.get('user_id')
    assert id == test_user_d['id']
    assert res.status_code== 200
    
    
@pytest.fixture
def token(test_user_d):
    return create_Jwt_Token({'user_id':test_user_d['id']})

@pytest.fixture
def authorized_user(client, token): 
    client.headers={
        **client.headers,
        'Authorization':f'Bearer {token}'
    }
    return client

@pytest.fixture
def test_post(test_user_d,session):
    postData=[
        {'title':'New', 'content':'nice', 'user_id':test_user_d['id']},
        {'title':'New1', 'content':'nice1', 'user_id':test_user_d['id']},
        {'title':'New2', 'content':'nice2', 'user_id':test_user_d['id']},
        {'title':'New3', 'content':'nice3', 'user_id':test_user_d['id']}
    ]
    
    def post_func(post):
        return models.Post(**post)
    post_map= map(post_func, postData)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts