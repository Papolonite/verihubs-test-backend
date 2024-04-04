from fastapi import APIRouter, Depends, HTTPException
from service.database import get_db
from schema.user import *
from sqlalchemy.orm import Session
from query import user as user_query
from service.password import hash_password, verify_password_matched


router = APIRouter(
  prefix='/api/users',
  tags=['users']
)

@router.post('/register', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

  if user.password != user.password_confirmation:
    raise HTTPException(status_code=400, detail='Password & Password Confirmation Not Matched')
  
  check_user = user_query.get_user_by_email(db, user.email)
  if check_user:
    raise HTTPException(status_code=400, detail='Email already registered in system')
  
  hashed_password = hash_password(user.password)
  
  new_user = user_query.create_user(db, user, hashed_password)
  
  response = User(id=new_user.id, email= new_user.email)
  return response

@router.post('/login', response_model=UserToken)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
  pass

# TODO: ADD GET CURRENT LOGGED IN USER