from fastapi import APIRouter, Depends
from database import get_db
from schema.user import *
from sqlalchemy.orm import Session


router = APIRouter(
  prefix='/api/users',
)

@router.post('/register', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  pass

@router.post('/login', response_model=UserToken)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
  pass