from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from app import database
from .. import models, schema, oauth
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote' , tags=['Vote'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def votes(vote:schema.Votes, db:Session = Depends(database.get_db), curr_user:int=Depends(oauth.get_cur_user)):
    post =db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'post {vote.post_id} does not exist' )

    vote_query =db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id ==curr_user.id )
    vote_found = vote_query.first()
    
    if vote.dir ==1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {curr_user.id} already voted on the post {vote.post_id}' )
        new_vote =models.Vote(post_id=vote.post_id, user_id=curr_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successful"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"vote deleted successfully"}
        