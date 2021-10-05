from sqlalchemy import Column, DateTime, Boolean

from ..database.conn import Base

class Scheduler_check(Base):
    __tablename__ = "scheduler_check"

    date = Column(DateTime, primary_key=True, index=True)
    is_call = Column(Boolean)
    

