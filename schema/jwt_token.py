from pydantic import BaseModel

class JWTTokenResponse(BaseModel):
  access_token: str
  token_type: str
    
