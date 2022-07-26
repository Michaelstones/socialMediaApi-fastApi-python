from fastapi import Depends, HTTPException, APIRouter , status, Response
from sqlalchemy.orm import Session
from .. import database,schema ,models, utils, oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authetication'])

@router.post('/login', response_model= schema.Token)
def login(user_Credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_Credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    
    verifyPWD = utils.verifyPWD(user_Credentials.password, user.password)
    
    if not verifyPWD:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')
    
    access_Token = oauth.create_Jwt_Token(data={'user_id':user.id})
    
    return {'access_Token':access_Token,'token_Type':'Bearer'}


