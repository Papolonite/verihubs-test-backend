from sqlalchemy import Column, Uuid, String
from sqlalchemy.orm import relationship
from database import Base
from uuid import uuid4
from association import user_tracked_coin_association

class User(Base):
  __tablename__ = 'users'
  
  id = Column(Uuid, primary_key=True, default=uuid4)
  email = Column(String(254), unique=True, index=True, nullable=False)
  password = Column(String, nullable=False)
  tracked_coins = relationship('Coin', secondary=user_tracked_coin_association, back_populates='users')
  