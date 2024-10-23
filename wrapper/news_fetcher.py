import requests
import json
import csv

from tqdm import tqdm

from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from time import sleep
from random import randint

from entity.entity import *


DEFAULT_IMAGE_URL: str = "https://www.gnu.ac.kr/images/web/main/sub_cnt/btype_vi_img12.png"
URL: str = "https://news.nate.com/recent"

header: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

class NewsFetcher:
    def __init__(self):
        self.news = None

        self.tags = {
            "politics" : ["정치", {"cate": "pol", "mid": "n201"}],
            # "economy": ["경제", {"cate": "eco", "mid": "n301"}],
            "social": ["사회", {"cate": "soc", "mid": "n401"}],
            # "international": ["국제", {"cate": "int", "mid": "n501"}],
            # "science_tech": ["과학/기술", {"cate": "its", "mid": "n601"}], 
        }
    
    
    def get_tag_id(self, tag_name: str):
        for tag in self.tags.keys():
            if self.tags[tag][0] == tag_name:
                return tag
        
        return None


    def fetch_news(self, n_pages: int=1) -> dict:
        NOW: str = datetime.now(tz=timezone(timedelta(hours=9))).strftime("%Y%m%d")

        self.news = {
            self.tags[tag][0] : []
            for tag in self.tags.keys()
        }

        for tag in tqdm(self.tags.keys()):
            articles: list[News] = []

            for page in tqdm(range(1, n_pages + 1)):
                args = self.tags[tag][1]
                list_url = URL + f'?cate={args["cate"]}&mid={args["mid"]}&type=c&date={NOW}&page={page}'
                response = requests.get(list_url, headers=header)
                bs = BeautifulSoup(response.text, 'html.parser')
                sleep(1 + randint(0, 10))

                for element in bs.findAll("div", "mduSubjectList"):
                    news_url: str = "https:" + element.select("a")[0]["href"].strip()

                    response = requests.get(news_url, headers=header)

                    date_str: str = element.find('span', "medium").find("em").text
                    pub_time = datetime.strptime("2024-" + date_str, '%Y-%m-%d %H:%M').isoformat()

                    content_bs = BeautifulSoup(response.text, features='html.parser').select("#realArtcContents")[0]

                    articles.append(
                        News(
                            title=element.find("h2", "tit").text.strip(),
                            content=content_bs.text.strip(),
                            image="https:" + element.find('img')["src"].strip() if element.find('img') else DEFAULT_IMAGE_URL,
                            url= news_url,
                            pub_time=pub_time,
                            tag=self.tags[tag][0],
                            press=element.find('span', "medium").text.split("\t")[0],
                        )
                    )

                sleep(1 + randint(0, 10))

            self.news[self.tags[tag][0]] = articles[:]
            print(self.tags[tag][0])

        return self.news


    def save_csv(self):
        for tag in self.news.keys():
            news = self.news[tag]
            news.insert(0, tuple(title for title in News._fields))

            with open(f"./news-{tag.replace('/', '-')}.csv", 'w', encoding="utf8") as f:
                csv.writer(f).writerows(news)
            
            print(tag)


    def load_csv(self) -> dict:
        self.news = {
            self.tags[tag][0] : []
            for tag in self.tags.keys()
        }

        for name in ("경제", "과학-기술", "국제", "라이프스타일", "사회", "정치"):
            try:
                f = open(f"./news-{name}.csv", 'r', encoding="utf8")
            except:
                continue

            for i in list(iter(csv.reader(f)))[1:]:
                self.news[name].append(
                    News(
                        title=i[0],
                        content=i[1],
                        url=i[2],
                        pub_time=i[3],
                        tag=i[4],
                        press=i[5],
                        image=i[6],
                    )
                )

            print(f"{name}")

        return self.news