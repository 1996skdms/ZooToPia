from sqlalchemy import sql
from sqlalchemy.orm import Session

from ..model import stock


def get_symbol(db: Session, name: str):
    name = "{}%".format(name)

    return db.query(stock.Stock).filter(sql.and_(stock.Stock.NAME.like(name)), stock.Stock.sector.not_like('nan')).first()