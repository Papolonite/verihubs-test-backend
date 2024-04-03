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
    
class UserTrackedCoin(BaseModel):
  tracked_coins: list[Coin] = []
  
  class Config:
    from_attributes = True
    
class AddTrackedCoin(BaseModel):
  coin_name_or_symbol : str