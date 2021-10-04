from typing import List, Optional

from pydantic import BaseModel


class Trade(BaseModel):
    id: int
    date: Optional[str] = None
    open: int
    high: int
    low: int
    close: int
    volume: int
    symbol: str

    class Config:
        orm_mode = True