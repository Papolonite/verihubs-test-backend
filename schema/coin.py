from pydantic import BaseModel, Field

class CoinBase(BaseModel):
  coin_id : str
  coin_symbol : str

class CoinCreate(CoinBase):
  pass

class CoinConvertedIDR(CoinBase):
  price_in_idr : float
    
class UserTrackedCoin(BaseModel):
  tracked_coins: list[CoinConvertedIDR] = []
    
class AddTrackedCoin(BaseModel):
  coin_name_or_symbol : str