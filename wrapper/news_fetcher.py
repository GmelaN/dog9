import requests
import json
import csv

from tqdm import tqdm

from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import re

from entity.entity import *

NOW: str = datetime.now(tz=timezone(timedelta(hours=9))).strftime("%Y%m%d%H%M")
# DEFAULT_IMAGE_URL: str = "https://i.namu.wiki/i/aemZBGJQLVu6ePeapyhYqE6OCJQId6CbI0WnQ6CqzTUJpHCO4EzLhRR4HZqy01pjxIA4AywnLqm_Ysw5A-9TJsbqpOKjEnK6rA5VjJf0phRNIhSIu7RINe2JsOzfiZ0pD5ySVhrKAixdSUX0a4xuEQ.webp"
DEFAULT_IMAGE_URL: str = "https://www.gnu.ac.kr/images/web/main/sub_cnt/btype_vi_img12.png"
N_PAGES = 1

header: dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

tags = {
    # "politics" : ["정치", 100],
    # "economy": ["경제", 101],
    "social": ["사회", 102],
    "lifestyle": ["라이프스타일", 103],
    # "international": ["국제", 104],
    # "science_tech": ["과학/기술", 105], 
}

def fetch_news() -> dict:
    news = {
        tags[tag][0] : []
        for tag in tags.keys()
    }

    for tag in tqdm(tags.keys()):
        articles: list[News] = []

        for page in tqdm(range(N_PAGES)):
            url = f"https://news.naver.com/section/template/SECTION_ARTICLE_LIST?sid={tags[tag][-1]}&sid2=&cluid=&pageNo={page}&date=&next={NOW}"
            response = requests.get(url, headers=header)
            bs = BeautifulSoup(json.loads(response.text)["renderedComponent"]["SECTION_ARTICLE_LIST"], features='html.parser')
            sleep(0.5 + randint(0, 100) * 0.1)

            for element in bs.findAll("li"):
                url: str = element.select("a")[0]["href"].strip()
                response = requests.get(url, headers=header)

                pub_time: str = element.select(".sa_text_datetime")[0].text.strip()

                if pub_time[-1:] == "전": # "xx분전"
                    numbers = int("".join(re.findall(r'\d+', pub_time)))

                    timestamp_utc = datetime.now(timezone.utc) - timedelta(minutes=numbers)
                    kst_time = timestamp_utc.astimezone(timezone(timedelta(hours=9)))
                    pub_time = kst_time.isoformat().split("+")[0]

                content_bs = BeautifulSoup(response.text, features='html.parser').select("#newsct_article")[0]

                articles.append(
                    News(
                        title=element.select("strong")[0].text.strip(),
                        # content=element.select(".sa_text_lede")[0].text.strip(),
                        content=content_bs.text.strip(),
                        image=content_bs.select("img")[0]["data-src"].strip() if content_bs.select("img") else DEFAULT_IMAGE_URL,
                        url=element.select("a")[0]["href"].strip(),
                        pub_time=pub_time,
                        tag=tags[tag][0],
                        press=element.select(".sa_text_press")[0].text.strip(),
                    )
                )

            sleep(0.5 + randint(0, 30))

        news[tags[tag][0]] = articles[:]
        print(tags[tag][0])
    return news
