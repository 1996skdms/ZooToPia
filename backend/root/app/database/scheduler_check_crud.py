from sqlalchemy.orm import Session

from ..model import scheduler_check as model
from ..schema import scheduler_check as schema

from datetime import datetime

def get_check(db: Session, date: datetime):
    return db.query(model.Scheduler_check).filter(model.Scheduler_check.date == date).first()

def create_check(db: Session, check: schema.Scheduler_check):

    db_check = model.Scheduler_check(date=check.date, is_call=check.is_call)

    db.add(db_check)
    db.commit()
    db.refresh(db_check)

    return db_check