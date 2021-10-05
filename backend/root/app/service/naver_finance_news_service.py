from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode, urlparse, urljoin, parse_qs

from datetime import datetime, timedelta

from pandas import DataFrame
from pytz import timezone
class Finance_news:

    url = 'https://finance.naver.com/item/news_news.nhn' 

    def crawler(self, company_code, max_page, custom_timedelta = timedelta(days=1)):

        query_param = {}
        query_param['code'] = company_code

        url_info = urlparse(self.url)
        df = DataFrame(columns={'pubDate','title','description'})
        for page in range(1, max_page+1):
            query_param['page'] = page
            query = urlencode(query_param)

            res = requests.get(self.url + '?' + query).text
            html = BeautifulSoup(res, "lxml")

            # print(html)

            title_tag = html.select('.title')

            titles = []
            links = []
            publishers = [ pub.get_text().strip() for pub in html.select('.info')]
            dates   = [date.get_text().strip()[:11].strip() for date in html.select('.date')]
            contents = []
            # ids = []
            

            now = datetime.now(timezone('Asia/Seoul'))
            today = datetime(now.year, now.month, now.day)

            # 각 내용별 형식 맞추기
            limit = 0
            for i in range(0, len(dates)):
                # newsdate = datetime.strptime(dates[i], "%Y.%m.%d %H:%M")
                newsdate = datetime.strptime(dates[i], "%Y.%m.%d")

                # 제한날짜 이내에 뉴스기사들만 넣기
                if (today - newsdate) >= custom_timedelta:
                    limit = i-1
                    break

                # title 가져오기
                tag = title_tag[i]
                titles.append(tag.a.get_text().strip())

                # link 가져오기
                urllink = urljoin(self.url,tag.a.get('href'))
                links.append(urllink)

                # content 가져오기
                content_res = requests.get(links[i]).text
                content_html = BeautifulSoup(content_res, "lxml")
                contents.append(content_html.select_one('#news_read').get_text())

                # 뉴스 식별자 가져오기( article_id, office_id )
                # ids.append(parse_qs(urlparse(urllink).query)['article_id'][0])

                limit = limit+1
            
            new_df = DataFrame({
                'pubDate' : dates[:limit+1],
                'title' : titles,
                'description' : contents
            })
            
            df=df.append(new_df, ignore_index=True)
        
        return df

finance_news = Finance_news()
