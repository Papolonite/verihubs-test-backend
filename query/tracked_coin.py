from sqlalchemy.orm import Session
from sqlalchemy import func
from model import user as user_model, tracked_coin as tracked_coin_model
from schema import tracked_coin as tracked_coin_schema

def get_tracked_coin(db: Session, user:user_model.User, coin_id_or_symbol: str):
  tracked_coin = db.query(tracked_coin_model.TrackedCoin).filter(tracked_coin_model.TrackedCoin.user_id == user.id)
  tracked_coin = tracked_coin.filter((tracked_coin_model.TrackedCoin.coin_id == coin_id_or_symbol) | (tracked_coin_model.TrackedCoin.coin_symbol == func.upper(coin_id_or_symbol)))

  if tracked_coin:
    return tracked_coin.first()
  return None

def add_tracked_coin(db: Session, user:user_model.User, data: tracked_coin_schema.CoinCreateRequest):
  new_coin = tracked_coin_model.TrackedCoin(coin_id= data.coin_id, coin_symbol = data.coin_symbol, user_id = user.id)
  
  db.add(new_coin)
  db.commit()
  db.refresh(new_coin)
  return new_coin 

def remove_tracked_coin(db: Session, coin:tracked_coin_model.TrackedCoin):
  db.delete(coin)
  db.commit()
  return coin

