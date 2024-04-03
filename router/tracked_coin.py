from fastapi import APIRouter, Depends
from schema.coin import *
from sqlalchemy.orm import Session
from service.database import get_db

router = APIRouter(
  prefix='/api/tracked_coin',
)

@router.get('/', response_model=UserTrackedCoin)
def get_list_tracked_coin(db: Session = Depends(get_db)):
  pass

@router.get('/{tracked_coin_id}', response_model=Coin)
def get_tracked_coin(tracked_coin_id: int, db: Session = Depends(get_db)):
  pass

@router.post('/', response_model=Coin)
def add_tracked_coin(coin: AddTrackedCoin, db: Session = Depends(get_db)):
  pass

@router.delete('/{tracked_coin_id}', response_model=Coin)
def delete_tracked_coin(tracked_coin_id: int, db: Session = Depends(get_db)):
  pass

