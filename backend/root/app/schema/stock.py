from typing import List, Optional

from pydantic import BaseModel

from ..schema.trade import Trade


class Stock(BaseModel):
    id: int
    symbol: str
    market: str
    NAME: str
    sector: str
    region: str

    class Config:
        orm_mode = True