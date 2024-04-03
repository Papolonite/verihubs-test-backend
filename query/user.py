from sqlalchemy.orm import Session
from model import model, schemas
import bcrypt


def get_user(db: Session, user_id: str):
  return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
  return db.query(model.User).filter(model.User.email == email).first()

def create_user(db: Session, data: schemas.UserCreate):
  hashed_password = bcrypt.hashpw(data.password, bcrypt.gensalt(14))
  check_matched = bcrypt.checkpw(data.password_confirmation, hashed_password)
  
  if check_matched:
    new_user = model.User(email = data.email, password= hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 
  return None

def login_user(db: Session, data: schemas.UserLogin):
  user = get_user_by_email(db, data.email)
  check_password_matched = bcrypt.checkpw(data.password, user.password)
  
  if check_password_matched:
    return user
  return None
  
def get_user_tracked_coin(db: Session, user_id: str):
  current_user = get_user(db=db, user_id=user_id)
  if current_user:
    return current_user.tracked_coins
  return None