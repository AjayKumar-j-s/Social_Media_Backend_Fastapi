from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .import models
from .database import engine 
from .routes import post,user,authenticate

models.Base.metadata.create_all(bind = engine)



app = FastAPI()



try:
    conn = psycopg2.connect(host = 'localhost',database='fastapi',user = 'postgres',password = 'sathyapriya',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database Connection was Successful")
except Exception as err:
    print("The Error was",err)
    time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authenticate.router)