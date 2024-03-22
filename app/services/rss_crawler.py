from app.services.base_crawler import WebsiteCrawler
from app.schemas.document_dto import DocumentDTO

from typing import List, Dict

import feedparser

from bs4 import BeautifulSoup


class RssCrawler(WebsiteCrawler):
    def __init__(self, base_url: str):
        self.base_url = base_url


    def fetch_documents(self) -> List[DocumentDTO]:
        """
        fetch documents from website
        
        :return: 문서의 리스트, 각 문서는 딕셔너리로 표현됨
        """

        feed_dict: feedparser.FeedParserDict = feedparser.parse(self.base_url)
        element_type: str = feed_dict["feed"]["title"]
        entries: feedparser.FeedParserDict = feed_dict["entries"]

        result: List[DocumentDTO] = list()

        for i in range(len(entries)):
            result.append(
                DocumentDTO(
                    title=entries[i]["title"],
                    content=BeautifulSoup(entries[i]["content"][0]["value"], "html").text.replace('\n', " "),
                    type=element_type,
                    category="news",
                    href=entries[i]["href"]
                )
            )

        return result



    def parse_document(self, html_content: str) -> Dict:
        """
        HTML 내용을 파싱하여 필요한 정보(예: 제목, 내용)를 추출하는 메소드.
        
        :param html_content: 파싱할 HTML 문서의 내용
        :return: 추출된 정보를 담은 딕셔너리
        """
        pass


    def crawl(self) -> List[DocumentDTO]:
        """
        크롤링 작업의 메인 메소드. `fetch_documents`를 호출하여 웹사이트로부터 문서를 가져온 뒤,
        `parse_document`를 사용하여 각 문서를 파싱함.
        
        :return: 파싱된 문서의 리스트, 각 문서는 딕셔너리로 표현됨
        """
        pass
