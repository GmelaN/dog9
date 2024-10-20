from typing import Literal
import requests
from tqdm import tqdm

from entity.entity import *
from constants import *

from urllib.parse import quote
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

            if response.status_code != 200:
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
            
        assert tag_id is not None
        response = self.send("/tag", method="POST", auth=True, data={"tagName": tag_name, "tagId": tag_id})

        if response.status_code != 200:
            raise RuntimeError("failed to upload tag: %s" % response.text)

        ApiWrapper.TAG_TABLE[tag_id] = tag_name

        return tag_id


    def upload_news(self, news: list[News]):
        for n in tqdm(news):
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
                raise RuntimeError("failed to upload news: %s" % response.text)


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
