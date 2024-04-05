from pydantic import BaseModel, UUID4
class UserBase(BaseModel):
  email: str

class UserLoginRequest(UserBase):
  password: str

class UserRegisterRequest(UserLoginRequest):
  password: str
  password_confirmation : str

class User(UserBase):
  id: UUID4

  class Config:
    from_attributes = True  

class UserRegisterResponse(BaseModel):
  message: str
  detail : User = {}
