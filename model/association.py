from sqlalchemy import Column, Uuid, Integer, Table, ForeignKey
from service.database import Base

user_tracked_coin_association = Table(
  'user_coin',
  Base.metadata,
  Column('user_id', Uuid, ForeignKey('users.id')),
  Column('tracked_coins_id', Integer, ForeignKey('coins.id'))
)