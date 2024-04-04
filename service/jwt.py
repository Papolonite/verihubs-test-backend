from datetime import datetime, timedelta, timezone
from config import *
from jose import JWTError, jwt


def create_access_token(user_id):
  iat = datetime.now(timezone.utc)
  exp = iat + timedelta(minutes= JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
  
  token_data = {
    'sub' : user_id,
    'iat' : iat,
    'exp' : exp
  }
  
  encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=JWT_ALGORITHM)
  return encoded_jwt

def parse_token(token):
  try:
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    expiry_date = decoded_token['exp']
    datetime_now_timestamp = int(datetime.timestamp(datetime.now(timezone.utc)))

    if expiry_date >= datetime_now_timestamp:
      return decoded_token
    return None
  except JWTError:
    return None