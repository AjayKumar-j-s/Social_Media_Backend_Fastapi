from fastapi import Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..import schemas
from ..import models
from ..import utils

router = APIRouter(
    prefix = "/users",
    tags= ['Users']
)




@router.post("/",response_model=schemas.UserOut)
def create(user:schemas.UserCreate,db :Session = Depends(get_db)):
    hash_pwd = utils.hash(user.password)
    user.password = hash_pwd
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

