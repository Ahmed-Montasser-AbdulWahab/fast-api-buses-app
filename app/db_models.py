from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Bus(Base):
    __tablename__ = "buses"
    lineNumber = Column(Integer, primary_key=True)
    with_slash = Column(Boolean, primary_key=True)
    starting = Column(String(255), index=False, nullable=False)
    destination = Column(String(255), index=False, nullable=False)
    garage = Column(String(255), index=False, nullable=True, default="N/A")


