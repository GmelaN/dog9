import feedparser

from typing import Dict, List, Tuple

import httpx
# from app.schemas.document_dto import DocumentDTO


from dataclasses import dataclass

from app.config.json_config_loader import JSONConfig

@dataclass(frozen=True)
class DocumentDTO:
    title: str
    content: str
    type: str
    category: str
    href: str


async def fetch_feed(type: str = "gnu") -> List[DocumentDTO]:
    JSONConfig.load_config(config_type="urls")
    urls: Dict[str, str] = JSONConfig.get_config(["gnu"])

    async with httpx.AsyncClient() as client:
        result: List[DocumentDTO] = []

        for key in urls.keys():
            url = urls[key]
            response = await client.get(url)

            parsed_dict: feedparser.FeedParserDict = feedparser.parse(response.text)

            entries: List = parsed_dict["entries"]
            channels: feedparser.FeedParserDict = parsed_dict["channel"]


            category: str = channels["title"]

            entry: feedparser.FeedParserDict
            for entry in entries:
                title = entry.title
                if "content" in entry.keys():
                    content = entry.content[0].value
                else:
                    content = entry.title_detail.value

                category = category
                href = entry.link
                result.append(DocumentDTO(title=title, content=content, type="", category=category, href=href))

        return result


# for debugging
if __name__ == "__main__":
    import asyncio

    result: List[DocumentDTO] = asyncio.run(fetch_feed())
    print(result[0])
