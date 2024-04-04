from sqlalchemy import Column, Uuid, String
from sqlalchemy.orm import relationship
from service.database import Base
from uuid import uuid4

class User(Base):
  __tablename__ = 'users'
  
  id = Column(Uuid, primary_key=True, default=uuid4)
  email = Column(String(254), unique=True, index=True, nullable=False)
  password = Column(String, nullable=False)
  tracked_coins = relationship('TrackedCoin', back_populates='users')
  