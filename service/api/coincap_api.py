import requests

base_url = 'https://api.coincap.io/v2'

def search_coin(coin_search_or_id: str):
  endpoint = f'{base_url}/assets'
  
  params = {
    'search' : coin_search_or_id,
    'limit' : 1
  }
  
  r = requests.get(endpoint, params=params)
  if r.status_code == 200:
    return r.json()
  return None

def get_coin_by_id(coin_id: str):
  endpoint = f'{base_url}/assets/{coin_id}'
  
  r = requests.get(endpoint)
  if r.status_code == 200:
    return r.json()
  return None

def get_rates(id: str):
  endpoint = f'{base_url}/rates/{id}'
  
  r = requests.get(endpoint)
  if r.status_code == 200:
    return r.json()
  return None
  
  
  