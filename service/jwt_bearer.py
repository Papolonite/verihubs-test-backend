from fastapi import HTTPException, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from typing_extensions import Annotated, Doc
from fastapi.security import HTTPBearer

from service.jwt import parse_token

class JWTBearer(HTTPBearer):
  def __init__(self, auto_error: bool = True):
    super(JWTBearer, self).__init__(auto_error=auto_error)
    
  async def __call__(self, request: Request):
    credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
    
    if credentials:
      if not credentials.scheme == "Bearer":
        raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
      if not self.verify_jwt(credentials.credentials):
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")
      return credentials.credentials
    else:
       raise HTTPException(status_code=403, detail="Invalid authorization code.")
     
  def verify_jwt(self, jwtoken: str) -> bool:
    try:
      payload = parse_token(jwtoken)
      
      if payload:
        return True
    except:
      return False
    return False