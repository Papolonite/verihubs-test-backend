from pydantic import BaseModel, Field

class CoinBase(BaseModel):
  coin_id : str
  coin_symbol : str

class CoinCreateRequest(CoinBase):
  pass

class AddTrackedCoinRequest(BaseModel):
  coin_name_or_symbol : str

class CoinConvertedIDR(CoinBase):
  price_in_idr : float
    
class UserTrackedCoinResponse(BaseModel):
  tracked_coins: list[CoinConvertedIDR] = []
    
class CoinResponse(BaseModel):
  message: str
  data: CoinBase