import uvicorn
from dataclasses import asdict
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.database import conf
from app.database.conn import db
from app.routers import stock
from app.routers import news


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
    app.include_router(news.router, prefix='/news', tags=['news'])

    return app


app = init_app()

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

# gunicorn main:app -k uvicorn.workers.UvicornWorker -p 8080:8080 -w 4
# docker run -itd -p 8080:8080 jinwoo6612/stocktest