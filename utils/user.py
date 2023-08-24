from database import models, schemas
from sqlalchemy.orm import Session
from utils.security import get_hashed_password, verify_password, create_access_token, decode_access_token

def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()

def get_current_user(token: str, db: Session):
    payload = decode_access_token(token)
    if not payload:
        return False
    user = get_user_by_id(payload["id"], db)
    if not user:
        return False
    return user
    

def create_new_user(user: schemas.UserCreate, db : Session):
    if get_user_by_email(user.email, db):
        return False
        
    hashed_password = get_hashed_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password, name=user.email.split("@")[0])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return create_access_token(new_user)
    


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email,db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return create_access_token(user)

def get_user_orders(token: str, db: Session):
    user = get_current_user(token, db)
    if not user:
        return False
    return db.query(models.Order).filter(models.Order.user_id == user.id).all()

def get_order_details(order_id: int, db: Session):
    db.query(models.OrderDetails).filter(models.OrderDetails.order_id == order_id).first()