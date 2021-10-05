from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.conn import db
from ..database import stock_posi_negative_crud as spn_crud, scheduler_check_crud as sch_check_crud
from ..schema import stock_posi_negative as spn_schema,  scheduler_check as sch_check_schema

from ..service import naver_finance_news_service as nfns, news_service

from datetime import datetime, timedelta
import time
from pytz import timezone

import pathlib
import os

router = APIRouter()

@router.get("/save")
async def saveDf(db: Session = Depends(db.get_db)):
    
    time.sleep(3)
    now = datetime.now(timezone('Asia/Seoul'))
    today = datetime(now.year, now.month, now.day)

    sch_check = sch_check_crud.get_check(db=db, date=today)
    if sch_check is None:
        sch_check_crud.create_check(db=db, check=sch_check_schema.Scheduler_check(date=today, is_call=True))

        # 카카오, 셀트리온, 삼성전자
        company_code = ['035720', '068270', '005930']
        # spn schema object list
        spn_list = []
        # 뉴스분석 object
        newsService = news_service.news_service   
        # naver finance cralwer
        nfns_crawler = nfns.finance_news

        for code in company_code:
            # 크롤링(종목코드, 최대 10페이지, 오늘부터 1일)
            df = nfns_crawler.crawler(code, 10, timedelta(days=2))
            # 형태소 분석
            df = newsService.morphs_nlp(df)
            # 긍부정율 예측
            predict_result = newsService.predict_score(df)
            df = predict_result['df']
            # 날짜별 정렬
            df = newsService.date_score(df)

            # SPN schema ojbect로 변환
            for j, row in df.iterrows():
                date = datetime.strptime(row.pubDate, "%Y.%m.%d")
                spn_list.append( spn_schema.Stock_posi_negative(code=code, date=date, score=row.score) )

        # date = datetime.strptime('2021.10.05', "%Y.%m.%d")
        # spn_list.append( spn_schema.Stock_posi_negative(code='123456', date=date, score=0.55555) )

        # db 저장
        spn_crud.create_span_list(db = db, spn_list=spn_list)

    return "SUCCESS"
