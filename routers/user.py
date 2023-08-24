from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils.user import create_new_user, authenticate_user, get_current_user
from utils.db import get_db
from database import schemas

router = APIRouter(prefix="/user", tags=["user"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def signup(response: Response, user: schemas.UserCreate, db: Session = Depends(get_db)):
    access_token = create_new_user(user,db)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    response.set_cookie(key= "Authorization", value=f"Bearer {access_token['access_token']}", httponly=True)
    return access_token
    

@router.post("/login", response_model=schemas.Token)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    access_token = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    response.set_cookie(key= "Authorization", value=f"{access_token['access_token']}", httponly=True)
    return access_token

@router.get("/me", response_model=schemas.User)
def read_users_me(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("Authorization")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    current_user = get_current_user(token,db)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return current_user
