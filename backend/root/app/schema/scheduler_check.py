from typing import List, Optional

from pydantic import BaseModel

from datetime import datetime

from ..schema.trade import Trade


class Scheduler_check(BaseModel):

    date : datetime
    is_call : bool

    class Config:
        orm_mode = True