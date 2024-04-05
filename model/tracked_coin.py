from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from service.database import Base

class TrackedCoin(Base):
  __tablename__ = 'tracked_coins'
  
  id = Column(Integer, primary_key=True, autoincrement=True)
  coin_id = Column(String, unique=True, nullable=False)
  coin_symbol = Column(String, unique=True, nullable=False)
  user_id = Column(ForeignKey('users.id'))
  
  users = relationship('User', back_populates='tracked_coins')
  
  __table_args__ = (UniqueConstraint('coin_id', 'coin_symbol', 'user_id',name='coin_user_uc'),
                     )