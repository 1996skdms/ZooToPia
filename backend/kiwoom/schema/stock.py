from pydantic import BaseModel

class Stock(BaseModel):
    id: int
    symbol: str
    market: str
    NAME: str
    sector: str
    region: str

    class Config:
        orm_mode = True
