from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from service.database import Base
from .association import user_tracked_coin_association

class Coin(Base):
  __tablename__ = 'coins'
  
  id = Column(Integer, primary_key=True, autoincrement=True)
  coin_id = Column(String, unique=True, nullable=False)
  coin_symbol = Column(String, unique=True, nullable=False)
  users = relationship('User', secondary=user_tracked_coin_association, back_populates='tracked_coins')