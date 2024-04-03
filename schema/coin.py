from pydantic import BaseModel

class CoinBase(BaseModel):
  coin_id : str
  coin_symbol : str

class CoinCreate(CoinBase):
  pass

class Coin(CoinBase):
  id : str
  
  class Config:
    from_attributes = True