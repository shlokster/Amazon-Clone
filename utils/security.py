from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from database import models, schemas



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def get_hashed_password(password,pwd_context=pwd_context):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password, pwd_context=pwd_context):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: models.User, expires_delta: Optional[timedelta] = None):
    user_schema_obj = schemas.User.from_orm(user)
    user_dict_obj = user_schema_obj.dict()
    token = jwt.encode(user_dict_obj, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return False

