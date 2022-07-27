from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase (BaseModel):
    title:str 
    content:str
    published:bool =True


class PostCreate(PostBase):
    pass

class UserRespon (BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
    class Config:
        orm_mode=True


class Post (PostBase):
    id:int
    user_id:int
    created_at:datetime
    owner:UserRespon
    
    
    
    class Config:
        orm_mode=True
    
    
    
   
class PP (BaseModel):
    title:str
    content:str
    created_at:datetime
    published:bool
    id:int
    user_id:int
    owner:UserRespon
    
    class Config:
        orm_mode=True
    
    
    
    
class PostOut (BaseModel):
    Post:PP
    vote:int 

    class Config:
        orm_mode=True
    
    
    
    
class UserSchema (BaseModel):
    email:EmailStr
    password:str




class UserLogin (BaseModel):
    email:EmailStr
    password:str
    
    
class Token(BaseModel):
    access_Token:str
    token_Type:str
    
    
class TokenData(BaseModel):
    id:Optional[str] = None
    
    
class Votes(BaseModel):
    post_id:int
    dir:conint(le=1)