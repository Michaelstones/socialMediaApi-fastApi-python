from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy import func
from .. import models, schema, utils, oauth
from sqlalchemy.orm import Session
from .. database import  get_db
from typing import List, Optional

router=APIRouter(prefix='/posts', tags=['Posts'])

# ,response_model=List[schema.Post]
@router.get('/' , response_model=List[schema.PostOut])
def get_post(db:Session=Depends(get_db),curr_user:int = Depends(oauth.get_cur_user), limit:int=10, skip:int=0, search:Optional[str]=''):
    # cur.execute(""" SELECT * FROM products."postsAPI" """)
    # post = cur.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result =db.query(models.Post, func.count(models.Vote.post_id).label('vote')).join(models.Vote,
                                                                                      models.Vote.post_id==models.Post.id,
                                                                                      isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(result)
    return result #posts
 
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)   
def creat_post(post:schema.PostCreate, db:Session=Depends(get_db), curr_user:int = Depends(oauth.get_cur_user)):
    # cur.execute(""" INSERT INTO products."postsAPI" (title, content, published) VALUES ( %s, %s, %s) RETURNING * """,(post.title, post.content,post.published))
    # post = cur.fetchone()
    # conn.commit()
    posts = models.Post(user_id=curr_user.id, **post.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts
    
    

    
@router.get('/{id}', status_code=status.HTTP_200_OK)   
def get_single_post(id:int, db:Session=Depends(get_db), curr_user:int = Depends(oauth.get_cur_user)):
    # cur.execute("""SELECT * FROM products."postsAPI" WHERE id=%s""",(str(id),))
    # post = cur.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    postsingle =db.query(models.Post, func.count(models.Vote.post_id).label('vote')).join(models.Vote,
                                                                                      models.Vote.post_id==models.Post.id,
                                                                                      isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if postsingle ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post with id {} not found'.format(id))
    
    return postsingle
    

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)   
def delete_single_post(id:int,db:Session=Depends(get_db), curr_user:int = Depends(oauth.get_cur_user)):
    # cur.execute("""DELETE FROM products."postsAPI" WHERE id=%s RETURNING * """,(str(id),))
    # post = cur.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post with id {} not found'.format(id))
    
    
    if post.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you are not authorized')
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', status_code=status.HTTP_200_OK,response_model=schema.Post)   
def update_single_post(id:int, post:schema.PostCreate,db:Session=Depends(get_db), curr_user:int = Depends(oauth.get_cur_user)):
    # cur.execute("""UPDATE products."postsAPI" SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    #             (post.title, post.content, post.published, str(id),))
    # post = cur.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id==id)
    posts = post_query.first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post with id {} not found'.format(id))
    
    if posts.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you are not authorized')
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()