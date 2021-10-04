import uvicorn
from dataclasses import asdict
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.database import conf
from app.database.conn import db
from app.routers import stock


def init_app():
    app = FastAPI()

    c = conf()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

    origins = ["*"]       # Frontend Origin

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
    app.include_router(stock.router, prefix='/stock', tags=['stocks'])

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

# gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8081 --workers 4 --daemon
# docker run -itd -p 8081:8081 jinwoo6612/stocktest