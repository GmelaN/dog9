from app.schemas.document_dto import DocumentDTO
from app.schemas.website_dto import WebsiteDTO

from abc import ABC, abstractmethod
from typing import List, Dict

class WebsiteCrawler(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def fetch_documents(self) -> List[Dict]:
        """
        fetch documents from website
        
        :return: 문서의 리스트
        """
        pass

    @abstractmethod
    def parse_document(self, html_content: str) -> Dict:
        """
        HTML 내용을 파싱하여 필요한 정보(예: 제목, 내용)를 추출하는 메소드.
        
        :param html_content: 파싱할 HTML 문서의 내용
        :return: 추출된 정보를 담은 딕셔너리
        """
        pass

    @abstractmethod
    def crawl(self) -> List[DocumentDTO]:
        """
        크롤링 작업의 메인 메소드. `fetch_documents`를 호출하여 웹사이트로부터 문서를 가져온 뒤,
        `parse_document`를 사용하여 각 문서를 파싱함.
        
        :return: 파싱된 문서의 리스트, 각 문서는 딕셔너리로 표현됨
        """
        pass
