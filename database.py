
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLITE_PATH = 'sqlite:///./coin_tracker.db'

db_engine = create_engine(
  SQLITE_PATH,
  connect_args = {
    "check_same_thread" : False
  }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()