from sqlalchemy.orm import Session
from model import user as user_model, tracked_coin as tracked_coin_model
from schema import coin as coin_schema
from sqlalchemy import or_, and_

def add_tracked_coin(db: Session, user:user_model.User, data: coin_schema.CoinCreate):
  new_coin = tracked_coin_model.TrackedCoin(coin_id= data.coin_id, coin_symbol = data.coin_symbol, user_id = user.id)
  
  db.add(new_coin)
  db.commit()
  db.refresh(new_coin)
  return new_coin 

def remove_tracked_coin(db: Session, user:user_model.User, coin_id_or_symbol: str):
  current_deleted_coin = db.query(tracked_coin_model.TrackedCoin).filter(and_(tracked_coin_model.TrackedCoin.user_id == user.id, 
      or_(tracked_coin_model.TrackedCoin.coin_id == coin_id_or_symbol, tracked_coin_model.TrackedCoin.coin_symbol == coin_id_or_symbol))).first()
  
  db.delete(current_deleted_coin)
  db.commit()
  return current_deleted_coin

