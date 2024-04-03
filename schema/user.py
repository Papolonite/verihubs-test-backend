from pydantic import BaseModel, UUID4
class UserBase(BaseModel):
  email: str

class UserLogin(UserBase):
  password: str

class UserCreate(UserLogin):
  password: str
  password_confirmation : str

class User(UserBase):
  id: UUID4

  class Config:
    from_attributes = True
    
class UserToken(BaseModel):
  token: str

    
