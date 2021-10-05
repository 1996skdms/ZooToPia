from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests

class Scheduler:

    def __init__(self):
        self.sch = AsyncIOScheduler()
        self.sch.start()
        self.job_id = 'finance news'

        # 23:50(KST) -> 14:50 (UTC)
        self.sch.add_job(self.getFinance, 'cron', hour=14, minute=50, second==10, max_instances=1)

        # 17:10(KST) -> 8:03 (UTC)
        # self.sch.add_job(self.getFinance, 'cron', hour=22, minute=19, second=10, max_instances=1)
        # self.sch.add_job(self.getFinance, 'interval', seconds=20, max_instances=1)

    async def getFinance(self):

        # production
        url = 'http://j5a602.p.ssafy.io:8080/naver/save'

        # develop
        # url = 'http://127.0.0.1:8080/naver/hi'
        r = requests.get(url)



