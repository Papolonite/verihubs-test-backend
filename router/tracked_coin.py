from fastapi import APIRouter, Depends, HTTPException
from requests import RequestException
from sqlalchemy.orm import Session


from service.authentication import get_current_user_data
from service.coincap import convert_coins_to_idr, search_coin
from service.database import get_db

import model.user as user_model
import query.tracked_coin as tracked_coin_query
import schema.tracked_coin as tracked_coin_schema

router = APIRouter(
  prefix='/api/tracked_coin',
  tags=['tracked_coin']
)

COINCAP_API_EXCEPTION = HTTPException(
  status_code=500,
  detail='Error while fetching data from coincap API'
)


@router.get('/', response_model=tracked_coin_schema.UserTrackedCoinResponse)
def get_list_tracked_coin(user : user_model.User = Depends(get_current_user_data), db: Session = Depends(get_db)):
  try:
    converted_coins = convert_coins_to_idr(user.tracked_coins)
  except RequestException:
    raise COINCAP_API_EXCEPTION
  return tracked_coin_schema.UserTrackedCoinResponse(tracked_coins=converted_coins)

@router.post('/', response_model=tracked_coin_schema.CoinResponse)
def add_tracked_coin(coin: tracked_coin_schema.AddTrackedCoinRequest, user : user_model.User = Depends(get_current_user_data), db: Session = Depends(get_db)):
  try:
    searched_coin = search_coin(coin.coin_name_or_symbol)
  except RequestException:
    raise COINCAP_API_EXCEPTION
  
  if searched_coin is None:
    raise HTTPException(
      status_code=404,
      detail='Coin cannot be found in Coincap API Database'
    )
  
  is_coin_exist = tracked_coin_query.get_tracked_coin(db, user, searched_coin.coin_id)
  if is_coin_exist:
    raise HTTPException(
      status_code=400,
      detail='Coin already tracked by user'
    )
  
  coin = tracked_coin_schema.CoinCreateRequest(coin_id=searched_coin.coin_id, coin_symbol=searched_coin.coin_symbol)
  created_coin = tracked_coin_query.add_tracked_coin(db, user, coin)
  coin_base = tracked_coin_schema.CoinBase(coin_id=created_coin.coin_id, coin_symbol=created_coin.coin_symbol)
  return tracked_coin_schema.CoinResponse(message= 'Successfully added coin to track list', data=coin_base)

@router.delete('/{tracked_coin_id_or_symbol}', response_model=tracked_coin_schema.CoinResponse)
def delete_tracked_coin(tracked_coin_id_or_symbol: str, user : user_model.User = Depends(get_current_user_data), db: Session = Depends(get_db)):
  coin = tracked_coin_query.get_tracked_coin(db, user, tracked_coin_id_or_symbol)
  print(coin)
  if coin is None:
    raise HTTPException(
      status_code=404,
      detail="Coin isn't tracked by user"
  )
  coin_base = tracked_coin_schema.CoinBase(coin_id=coin.coin_id, coin_symbol=coin.coin_symbol)
  tracked_coin_query.remove_tracked_coin(db, coin)
  return tracked_coin_schema.CoinResponse(message= 'Successfully deleted coin from track list', data=coin_base)