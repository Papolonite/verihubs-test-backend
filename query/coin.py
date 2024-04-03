from sqlalchemy.orm import Session
from model import model, schemas

def create_coin(db: Session, data: schemas.CoinCreate):
  new_coin = model.Coin(coin_id= data.coin_id, coin_symbol= data.coin_symbol)
  db.add(new_coin)
  db.commit()
  db.refresh(new_coin)
  return new_coin 

def get_coin(db: Session, id: str):
  return db.query(model.Coin).filter(model.Coin.id == id).first()

def get_coin_by_coin_id(db: Session, id: str):
  return db.query(model.Coin).filter(model.Coin.coin_id == id).first()

def get_coin_by_coin_symbol(db: Session, id: str):
  return db.query(model.Coin).filter(model.Coin.coin_symbol == id).first()
