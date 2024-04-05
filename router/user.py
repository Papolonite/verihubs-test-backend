from fastapi import APIRouter, Depends, HTTPException
from service.authentication import email_validation, password_validation
from service.database import get_db
from sqlalchemy.orm import Session

import schema.user as user_schema
import query.user as user_query

from service.jwt import create_access_token
from service.password import hash_password, verify_password_matched
from schema.jwt_token import JWTTokenResponse

router = APIRouter(
  prefix='/api/users',
  tags=['users']
)

@router.post('/register', response_model=user_schema.UserRegisterResponse)
def create_user(user: user_schema.UserRegisterRequest, db: Session = Depends(get_db)):

  email_validation_check = email_validation(user.email)
  if not email_validation_check:
    raise HTTPException(status_code=400, detail='Invalid Email format')
  
  if user.password != user.password_confirmation:
    raise HTTPException(status_code=400, detail='Password & Password Confirmation Not Matched')
  
  password_validation_check = password_validation(user.password)
  
  if not password_validation_check:
    raise HTTPException(status_code=400, detail='Password must have minimum 8 characters, at least one upper case letter, one lower caseletter, one number and one special character')
    
  check_user = user_query.get_user_by_email(db, user.email)
  if check_user:
    raise HTTPException(status_code=400, detail='Email already registered in system')
  
  hashed_password = hash_password(user.password)
  
  new_user = user_query.create_user(db, user, hashed_password)
  
  user = user_schema.User(id=new_user.id, email= new_user.email)
  response = user_schema.UserRegisterResponse(message='Successfully created new user', detail=user)
  return response

@router.post('/login', response_model=JWTTokenResponse)
def login_user(user: user_schema.UserLoginRequest, db: Session = Depends(get_db)):
  incorrect_credential_exception = HTTPException(
    status_code=401,
    detail='Incorrect email or password',
    headers={"WWW-Authenticate": "Bearer"}
  )
  
  user_db = user_query.get_user_by_email(db, user.email)
  if not user_db:
    raise incorrect_credential_exception
  
  hashed_password = user_db.password
  
  if not verify_password_matched(user.password, hashed_password):
    raise incorrect_credential_exception
  
  access_token = create_access_token(str(user_db.id))
  return JWTTokenResponse(access_token=access_token, token_type='bearer')