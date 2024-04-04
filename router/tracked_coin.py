from fastapi import APIRouter, Depends
import query.tracked_coin as query_tracked_coin
from schema.coin import *
from sqlalchemy.orm import Session
from service.authentication import get_current_user_data
from service.coincap import convert_coins_to_idr, search_coin
from service.database import get_db
from model.user import User as UserModel

router = APIRouter(
  prefix='/api/tracked_coin',
  tags=['tracked_coin']
)

@router.get('/', response_model=UserTrackedCoin)
def get_list_tracked_coin(user : UserModel = Depends(get_current_user_data), db: Session = Depends(get_db)):
  converted_coins = convert_coins_to_idr(user.tracked_coins)
  return UserTrackedCoin(tracked_coins=converted_coins)

@router.post('/', response_model=CoinBase)
def add_tracked_coin(coin: AddTrackedCoin, user : UserModel = Depends(get_current_user_data), db: Session = Depends(get_db)):
  searched_coin = search_coin(coin.coin_name_or_symbol)
  coin = CoinCreate(coin_id=searched_coin.coin_id, coin_symbol=searched_coin.coin_symbol)
  created_coin = query_tracked_coin.add_tracked_coin(db, user, coin)
  return CoinBase(coin_id=created_coin.coin_id, coin_symbol=created_coin.coin_symbol)

@router.delete('/{tracked_coin_id_or_symbol}', response_model=CoinBase)
def delete_tracked_coin(tracked_coin_id_or_symbol: str, user : UserModel = Depends(get_current_user_data), db: Session = Depends(get_db)):
  deleted_coin = query_tracked_coin.remove_tracked_coin(db, user, tracked_coin_id_or_symbol)
  return CoinBase(coin_id=deleted_coin.coin_id, coin_symbol=deleted_coin.coin_symbol)