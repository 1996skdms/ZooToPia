from sqlalchemy import Column, Integer, String

from ..database.conn import Base

class Hoga(Base):
    __tablename__ = "hoga"

    ordering = Column(Integer, primary_key=True)
    symbol = Column(String, primary_key=True)
    ask_price = Column(String)
    ask_volume = Column(String)
    bid_price = Column(String)
    bid_volume = Column(String)

