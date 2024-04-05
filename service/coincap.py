
from model.tracked_coin import TrackedCoin
from schema.tracked_coin import CoinConvertedIDR
import service.api.coincap_api as coincap_api
from schema.tracked_coin import CoinBase

def convert_coins_to_idr(user_tracked_coin: list[TrackedCoin]):
  idr_exchange_rate = float(coincap_api.get_rates('indonesian-rupiah')['data']['rateUsd'])
  list_converted_coin :  list[CoinConvertedIDR] = []
  
  for coin in user_tracked_coin:
    coin_exchange_rate = float(coincap_api.get_rates(coin.coin_id)['data']['rateUsd'])
    coin_converted_idr = CoinConvertedIDR(
      id=coin.id,
      coin_id=coin.coin_id,
      coin_symbol=coin.coin_symbol,
      price_in_idr=coin_exchange_rate / idr_exchange_rate
    )
    list_converted_coin.append(coin_converted_idr)
    
  return list_converted_coin
    
def search_coin(coin_user_id: str):
  searched_coin = coincap_api.search_coin(coin_user_id)
  
  if searched_coin:
    searched_coin = searched_coin['data']
    print(searched_coin)
    if len(searched_coin) != 0:
      return CoinBase(coin_id = searched_coin[0]['id'], coin_symbol=searched_coin[0]['symbol'])

  return None
    