from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .router import post, user,auth, vote
from .config import setting
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

      
my_post =[{'title':'New Entry', 'content':'nice working with fastapi'}, {'title':'second Entry', 'content':'nice working with postgres'}]
@app.get("/")
async def root():
    return {'message':'hello'}

@app.get('/sql')
def get_post(db:Session=Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {'data':posts}

app.include_router(post.router)
    
# user Tablee Query

app.include_router(user.router)

#auth router
app.include_router(auth.router)

#vote router
app.include_router(vote.router)

    
