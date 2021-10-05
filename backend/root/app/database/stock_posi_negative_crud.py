from sqlalchemy.orm import Session

from ..model import stock_posi_negative as spn_model
from ..schema import stock_posi_negative as spn_schema

from datetime import datetime

from typing import Iterable

def get_spn(db: Session, code: str, date: datetime):
    return db.query(spn_model.Stock_posi_negative).filter(spn_model.Stock_posi_negative.code == code, spn_model.Stock_posi_negative.date == date).first()

def create_spn(db: Session, spn: spn_schema.Stock_posi_negative):

    db_spn = spn_model.Stock_posi_negative(code=spn.code, date=spn.date, score=spn.score)

    db.add(db_spn)
    db.commit()
    db.refresh(db_spn)

    return db_spn

def create_span_list(db: Session, spn_list: Iterable[spn_schema.Stock_posi_negative]):

    db_list = []
    for spn in spn_list:

        db_list.append( spn_model.Stock_posi_negative(code=spn.code, date=spn.date, score=spn.score) )

    db.bulk_save_objects(db_list)
    db.commit()
    
    return db_list