from fastapi import Depends, HTTPException
from jose import JWTError
from service.database import get_db
from service.jwt import parse_token
from query.user import get_user
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

import re


from service.jwt_bearer import JWTBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login", scheme_name="JWT")

unauthorized_exception = HTTPException(
  status_code=401,
  detail='Unauthorized',
  headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user_data(token =  Depends(JWTBearer()), db: Session = Depends(get_db)):
  try:
    decoded_token = parse_token(token)
    
    user_id: str = decoded_token['sub']
    
    if user_id is None:
      raise unauthorized_exception

  except JWTError:
    raise unauthorized_exception
  
  user = get_user(db=db, user_id=UUID(user_id))
  if user is None:
    raise unauthorized_exception
  return user
  
def email_validation(email: str):
  validate = re.search("[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", email)
  
  if validate:
    return True
  else:
    return False
  
def password_validation(password: str):
  REGEX_VALIDATION = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$'
  
  validate = re.search(REGEX_VALIDATION, password)
  if validate:
    return True
  return False
  