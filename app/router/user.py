from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from .. import models, schema, utils
from sqlalchemy.orm import Session
from .. database import  get_db


router=APIRouter(prefix='/users', tags=['Users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserRespon)
def create_User( user:schema.UserSchema,db:Session=Depends(get_db)):
    hashed_pd = utils.hashPW(user.password)
    user.password = hashed_pd
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schema.UserRespon)
def get_user(id:str, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user does not exist')
    
    return user