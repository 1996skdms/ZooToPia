from sqlalchemy import sql
from sqlalchemy.orm import Session

from ..model import stock, hoga


def get_symbol(db: Session, name: str):
    name = "{}%".format(name)

    return db.query(stock.Stock).filter(sql.and_(stock.Stock.NAME.like(name)), stock.Stock.sector.not_like('nan')).first()

def get_hoga(db: Session, symbol: str):
    return db.query(hoga.Hoga).filter(hoga.Hoga.symbol == symbol).order_by(hoga.Hoga.ordering.asc()).all()


# .filter(hoga.Hoga.symbol == symbol)