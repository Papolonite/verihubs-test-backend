from sqlalchemy import Column, UniqueConstraint, Uuid, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from uuid import uuid4

user_tracked_coin_association = Table(
  'user_coin',
  Base.metadata,
  Column('user_id', Uuid, ForeignKey('users.id')),
  Column('tracked_coins_id', Integer, ForeignKey('coins.id'))
)

class User(Base):
  __tablename__ = 'users'
  
  id = Column(Uuid, primary_key=True, default=uuid4)
  email = Column(String(254), unique=True, index=True, nullable=False)
  password = Column(String, nullable=False)
  tracked_coins = relationship('Coin', secondary=user_tracked_coin_association, back_populates='users')
  
class Coin(Base):
  __tablename__ = 'coins'
  
  id = Column(Integer, primary_key=True, autoincrement=True)
  coin_id = Column(String, unique=True, nullable=False)
  coin_symbol = Column(String, unique=True, nullable=False)
  users = relationship('User', secondary=user_tracked_coin_association, back_populates='tracked_coins')