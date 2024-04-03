from pydantic import BaseModel
from schema.coin import CoinBase

class UserBase(BaseModel):
  email: str

class UserLogin(UserBase):
  password: str

class UserCreate(UserLogin):
  password: str
  password_confirmation : str

class User(UserBase):
  id: str

  class Config:
    from_attributes = True
    
class UserTrackedCoin(BaseModel):
  id: str
  tracked_coins: list[CoinBase] = []
  
  class Config:
    orm_mode = True