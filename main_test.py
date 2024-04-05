from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from service.database import get_db, Base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./coin_tracker_test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def register_user(email, password):
  response = client.post(
    '/api/users/register',
    json={
      'email' : email,
      'password' : password,
      'password_confirmation' : password
    }
  )
  return response

def login_user(email, password):
  response = client.post(
    '/api/users/login',
    json={
      'email' : email,
      'password' : password
    }
  )
  return response
  
def login_and_get_access_token(email, password):
  response = login_user(email=email, password=password)
  data = response.json()
  return data['access_token']

def test_create_user(test_db):
  email = 'testClient@gmail.com'
  password = 'Test!ng1234'
  
  response = register_user(email, password)
  assert response.status_code == 200
  
  data = response.json()

  user_detail= data['detail']
  assert user_detail['email'] == email
  assert 'id' in user_detail
  
def test_login_user(test_db):
  email = 'testClient@gmail.com'
  password = 'Test!ng1234'
  
  register_user(email, password)
  response = login_user(email, password)
  
  assert response.status_code == 200
  
  data = response.json()
  assert 'access_token' in data
  assert 'token_type' in data
  
def test_add_get_delete_coin(test_db):
  email = 'testClient@gmail.com'
  password = 'Test!ng1234'
  
  register_user(email, password)
  token = f'Bearer {login_and_get_access_token(email, password)}'
  
  # Add Coin
  response_btc = client.post(
    '/api/tracked_coin',
    headers= {'Authorization' : token},
    json={
      'coin_name_or_symbol' : 'btc',
      'password' : password
    }
  )
  
  assert response_btc.status_code == 200
  response_json = response_btc.json()
  assert 'message' in response_json
  data = response_json['data']
  assert data['coin_id'] == 'bitcoin'
  assert data['coin_symbol'] == 'BTC'
  
  # Get Coin After Add
  response_get_after_add = client.get(
    '/api/tracked_coin',
    headers= {'Authorization' : token}
  )
  
  assert response_get_after_add.status_code == 200
  response_json = response_get_after_add.json()
  assert 'tracked_coins' in response_json
  assert len(response_json['tracked_coins']) == 1 
  
  # Delete Coin
  response_delete = client.delete(
    '/api/tracked_coin/btc',
    headers= {'Authorization' : token}
  )
  
  assert response_delete.status_code == 200
  response_json = response_delete.json()
  assert 'message' in response_json
  data = response_json['data']
  assert data['coin_id'] == 'bitcoin'
  assert data['coin_symbol'] == 'BTC'
  
  # Get Coin After Delete
  response_get_after_delete = client.get(
    '/api/tracked_coin',
    headers= {'Authorization' : token}
  )
  
  assert response_get_after_delete.status_code == 200
  response_json = response_get_after_delete.json()
  assert 'tracked_coins' in response_json
  assert len(response_json['tracked_coins']) == 0 
  
  
  
  