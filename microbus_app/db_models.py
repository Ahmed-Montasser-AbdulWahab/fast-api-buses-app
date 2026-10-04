from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class MicroBus(Base):
    __tablename__ = "microbuses"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    starting = Column(String(255), index=False, nullable=False)
    destination = Column(String(255), index=False, nullable=False)


