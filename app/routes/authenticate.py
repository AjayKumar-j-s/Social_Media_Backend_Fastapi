from fastapi import Depends,APIRouter,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database
from .. import schemas
from .. import models,utils,oauth2

router = APIRouter(
    tags = ['authenticate']
)


@router.post("/login",response_model=schemas.Token)
def login(user :OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):

    u = db.query(models.User).filter(models.User.email == user.username).first()

    if not u:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    if not utils.verifyHash(user.password,u.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Creadentials")
    
    access_token = oauth2.create_access_token({"user_id" : u.id})
    return {"access_token" :access_token,"token_type":"bearer"}
    
    