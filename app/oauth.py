from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException , status
from datetime import datetime, timedelta
from app import models
from . import schema, database
from sqlalchemy.orm import Session
from .config import setting

SECRET_KEY= setting.secret_key
ALGO= setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expiry

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_Jwt_Token (data:dict):
    encoded_co = data.copy()
    expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_co.update({'exp':expire})
    encoded_jwt= jwt.encode(encoded_co, SECRET_KEY, algorithm=ALGO)
    return encoded_jwt

def verify_Token(token:str, credentials_exception):
    try: 
        check = jwt.decode(token, SECRET_KEY, ALGO)
        id:str = check.get('user_id')
        if id is None:
            raise credentials_exception
    
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    2
def get_cur_user(token:str= Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'could not validate',
                                          headers={"WWW-Authenticate":"Bearer"} )
    token = verify_Token(token, credentials_exception)
    user= db.query(models.User).filter(models.User.id==token.id).first()
    return user
    