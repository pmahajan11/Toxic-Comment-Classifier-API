# Importing packages

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# psycopg2 error fixes:
# link 1: https://stackoverflow.com/questions/11618898/pg-config-executable-not-found
# link 2: https://stackoverflow.com/a/26045938
# export DYLD_LIBRARY_PATH=/Users/pranav/Desktop/PostgreSQL/lib:$DYLD_LIBRARY_PATH 

from app import models
from app.database import engine
from app.routers import user, auth, comment
from app.config import settings

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(comment.router)


@app.get("/")
def root():
    return {"message": "Hello! This is a Toxic Comment Classifier API."}



