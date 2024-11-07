from typing import Literal
import requests
from tqdm import tqdm

import csv

from entity.entity import *
from constants import *

from urllib.parse import quote
from datetime import datetime, timezone, timedelta


class ApiWrapper:
    TOKEN: str = ""
    URL: str = ""
    AUTH: dict = {}
    TAG_TABLE: dict = {}

    def __init__(self, url=URL_):
        ApiWrapper.URL = url
        ApiWrapper.AUTH = AUTH

        if AUTH:
            self.login()
            self.refresh_tag_table()


    def register(self):
        response = self.send("/auth/eula", method="GET", auth=False)
        eulas = [eula["eulaId"] for eula in response.json()["data"]]

        payload = {
            "userId": ApiWrapper.AUTH["userId"],
            "password": ApiWrapper.AUTH["password"],
            "userNm": "LLM_TEST",
            "gender": "MALE",
            "birthDate": "2001-08-16",
            "interestTagIds": [
                "test_tag"
            ],
            "agreedEulaIds": eulas
        }

        response = self.send("/auth/sign-up", method="POST", auth=False, data=payload)

        if response.status_code == 200:
            return self.login()
        
        return response.status_code


    def login(self):
        response = self.send("/auth/token", method="POST", auth=False, data=ApiWrapper.AUTH)

        if response.status_code == 200:
            ApiWrapper.TOKEN = response.json()["data"][0]["accessToken"]

        return ApiWrapper.TOKEN


    def upload_journal(self, journal_name: str) -> str:
        uploaded_journals = self.get_uploaded_journals()
        journal: str = self.get_journal_id(uploaded_journals, journal_name)

        if journal is None:
            journal_id =  "%04d" % (len(uploaded_journals) + 1)
            response = self.send("/journal", method="POST", auth=True, query_str=True, data={"journalId": journal_id, "journalNm": journal_name})

            if response.status_code != 200 and ("errorCode" in response.json().keys() and response.json()["errorCode"] != "news.alreadyJournalExists"):
                raise RuntimeError("failed to upload journal: %s" % response.text)

        else:
            journal_id = journal.journalId

        return journal_id


    def get_uploaded_journals(self) -> list[Journal]:
        response = self.send("/journal", method="GET", auth=True)
        if response.status_code != 200:
            raise RuntimeError("unable to fetch uploaded journal: %s" % response.text)


        journals: list[Journal] = []
        for journal in response.json():
            journals.append(Journal(journalNm=journal["journalNm"], journalId=journal["journalId"]))

        return journals


    def get_uploaded_tags(self):
        response = self.send("/tag", method="GET", auth=True)
        if response.status_code != 200:
            raise RuntimeError("unable to fetch uploaded tag(s): %s" % response.text)

        tags: list[Tag] = []
        for tag in response.json():
            tags.append(Tag(tagId=tag["tagId"], tagName=tag["tagName"]))
        
        return tags
    

    def refresh_tag_table(self):
        ApiWrapper.TAG_TABLE = {}
        tags = self.get_uploaded_tags()

        for tag in tags:
            ApiWrapper.TAG_TABLE[tag.tagId] = tag.tagName

        return ApiWrapper.TAG_TABLE
    

    def upload_tag(self, tag_name: str, tag_id: str|None=None):
        self.refresh_tag_table()
        
        for tag in ApiWrapper.TAG_TABLE.keys():
            if tag_name == ApiWrapper.TAG_TABLE[tag]:
                return tag
            
        if tag_id is None:
            raise RuntimeError(f"Please upload {tag_name}!")
        response = self.send("/tag", method="POST", auth=True, data={"tagName": tag_name, "tagId": tag_id})

        if response.status_code != 200:
            raise RuntimeError("failed to upload tag: %s" % response.text)

        ApiWrapper.TAG_TABLE[tag_id] = tag_name

        return tag_id


    def upload_news(self, news: dict) -> list[UploadedNews]:
        uploaded_news: list[UploadedNews] = []

        for tag in tqdm(news.keys()):
            for n in tqdm(news[tag]):
                journal_id = self.upload_journal(n.press)
                tag_id = self.upload_tag(n.tag)

                data = {
                    "title": n.title,
                    "link": n.url,
                    "journalId": journal_id,
                    "publicationDate": n.pub_time,
                    "photoLink": n.image,
                    "tagIds": [tag_id]
                }

                response = self.send("/news", method="POST", auth=True, data=data)

                if response.status_code != 200:
                    self.save_csv(uploaded_news)
                    raise RuntimeError("failed to upload news: %s" % response.text)
                
                uploaded_news.append(
                    UploadedNews(
                        id=response.json()["data"][0]["newsIdx"],
                        title=n.title,
                        content=n.content,
                        url=n.url,
                        pub_time=n.pub_time,
                        tag=n.tag,
                        press=n.press,
                        image=n.image
                    )
                )

        self.save_csv(uploaded_news)
        return uploaded_news
    

    def save_csv(self, uploaded_news: list):
        uploaded_news.insert(0, tuple(title for title in UploadedNews._fields))

        with open(f"./news-uploaded.csv", 'w', encoding="utf8") as f:
            csv.writer(f).writerows(uploaded_news)
        
        uploaded_news.pop(0)
    
    
    def load_csv(self) -> list[UploadedNews]:
        uploaded_news: list[UploadedNews] = []

        with open(f"./news-uploaded.csv", 'r', encoding="utf8") as f:
            file = csv.reader(f)
            next(file)

            for row in file: # id,title,content,url,pub_time,tag,press,image
                uploaded_news.append(
                    UploadedNews(
                        id=row[0],
                        title=row[1],
                        content=row[2],
                        url=row[3],
                        pub_time=row[4],
                        tag=row[5],
                        press=row[6],
                        image=row[7],
                    )
                )
        
        return uploaded_news


    def download_news(self) -> News:
        response = self.send("/news", method="GET", auth=True)

        if response.status_code != 200:
            raise RuntimeError("failed to fetch news: %s" % response.text)

        return response.json()['data']


    def send(self, endpoint: str, method: Literal["GET", "POST"]="GET", auth: bool=True, data: dict={}, query_str: bool=False) -> requests.Response:
        headers = {
            "Content-Type": "application/json",
        }

        url = ApiWrapper.URL + endpoint

        if auth:
            if len(ApiWrapper.TOKEN) == 0:
                self.login()

            headers["Authorization"] = "Bearer " + ApiWrapper.TOKEN

        if method == "POST":
            if query_str:
                response = requests.post(url=url, headers=headers, params=data)
            else:
                response = requests.post(url=url, headers=headers, json=data)
            
        # elif method == "GET":

        else: # default: GET
            if query_str:
                response = requests.get(url=url, headers=headers, params=data)
            else:
                response = requests.get(url=url, headers=headers, json=data)
            
        return response


    def get_journal_name(self, journals: list[Journal], id: int) -> Journal:
        for journal in journals:
            if journal.journalId == id:
                return journal
            
        return None


    def get_journal_id(self, journals: list[Journal], name: str) -> Journal:
        for journal in journals:
            if journal.journalNm == name:
                return journal

        return None


    def upload_article(self, article: Article) -> requests.Response:
        response = self.send(
            "/article",
            method="POST",
            auth=True,
            data={
            "title": article.title,
            "content": article.content,
            "publicationDate": datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "newsIdxes": article.news_id,
            }
        )


        if response.status_code != 200:
            raise RuntimeError("failed to upload journal: %s" % response.text)

        return response
