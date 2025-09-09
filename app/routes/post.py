
from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db,SessionLocal,engine
from ..import schemas
from ..import models
from ..import utils,oauth2




router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)



@router.get("/",response_model=List[schemas.Post])
def post(db:Session = Depends(get_db),user_id : int = 
          Depends(oauth2.get_current_user)):
    query_post = db.query(models.Post).all()

    return query_post


@router.get("/{id}")
def get_post(id:int,db:Session = Depends(get_db),user_id : int = 
          Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if(post):
        return {"data":post}
    
    if(post.owner_id != user_id.id):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post of id {id} not found")
        
        



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# def posts(payload:dict = Body(...)):
def posts(post : schemas.PostCreate,db :Session = Depends(get_db),user_id : int = 
          Depends(oauth2.get_current_user)):
        new_post = models.Post(owner_id = user_id.id,**post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post


        

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def post(id:int,db :Session = Depends(get_db),user_id : int = 
          Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        return Response(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not Authorized to perform action")
    
    if(post.owner_id != user_id.id):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@router.put("/{id}")
def update(id:int,post:schemas.PostCreate,db :Session = Depends(get_db),user_id : int = 
          Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id)
    if(db_post.first() is None):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    if(post.owner_id != user_id.id):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    
    db_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data":db_post.first()}


