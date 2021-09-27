import os
import sys
import uvicorn
from dataclasses import asdict
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import stock
from config.database import conf
from database.conn import db

def init_app():
    app = FastAPI()

    c = conf()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

    origins = [
        "http://localhost:5000",  # Frontend Origin
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[],
        max_age=3600,
    )
    # 라우터
    app.include_router(stock.router, prefix='/kiwoom', tags=['stocks'])

    return app                              # need return

app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)







