from app import schema
import pytest
from jose import jwt
from app.config import settings
from tests.database import client

@pytest.fixture()
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
    

# def test_root(client):
#     res =client.get('/')
#     print(res.json().get('message'))
    
def test_user(client):
    res = client.post('/users/', json={'email':'mick@gmail.com', 'password':'mickshow'})
    new_user=schema.UserRespon(**res.json())
    assert new_user.email== 'mick@gmail.com'
    assert res.status_code==201
    
    
def test_user_login(client, test_user_d):
    res = client.post('/login', data={'username':test_user_d['email'], 'password':test_user_d['password']})
    login_validate = schema.Token(**res.json())
    check = jwt.decode(login_validate.access_Token, settings.secret_key, settings.algorithm)
    id:str = check.get('user_id')
    assert id == test_user_d['id']
    assert res.status_code== 200


@pytest.mark.parametrize('email, password, status_code', [
    ('mick@gmail.com', 'ruwfewf',403),
    ('micsk@gmail.com', 'mickshow',403),
    ('micsk@gmail.com', 'mirkkr',403),
    (None, 'ruwfewf',422),
    ('micsk@gmail.com', None,422),
])
def test_failed_login(test_user_d, client, email, password, status_code):
    res= client.post('/login', data={'username':email, 'password':password})
    assert res.status_code==status_code
    # assert res.json().get('detail')=='Invalid credentials'