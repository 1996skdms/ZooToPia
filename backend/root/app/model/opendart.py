from sqlalchemy import Column, String

from ..database.conn import Base

class Opendart(Base):
    __tablename__ = "opendart"

    corp_code = Column(String, primary_key=True, index=True)
    corp_name = Column(String)
    stock_code = Column(String)
    modify_date = Column(String)

