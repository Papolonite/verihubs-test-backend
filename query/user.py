from sqlalchemy.orm import Session
from model import user as user_model

from schema import user as user_schema


def get_user(db: Session, user_id: str):
  return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
  return db.query(user_model.User).filter(user_model.User.email == email).first()

def create_user(db: Session, data: user_schema.UserCreate, hashed_password: str):
  new_user = user_model.User(email = data.email, password= hashed_password)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user 
  
def get_user_tracked_coin(db: Session, user_id: str):
  current_user = get_user(db=db, user_id=user_id)
  if current_user:
    return current_user.tracked_coins
  return None