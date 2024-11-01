from collections import namedtuple

News = namedtuple("News", ["title", "content", "url", "pub_time", "tag", "press", "image"])
SummerizedNews = namedtuple("SummerizedNews", ["title", "content", "topics", "id"])
UploadedNews = namedtuple("News", ["id", "title", "content", "url", "pub_time", "tag", "press", "image"])
Article = namedtuple("Article", ["title", "content", "news_id"])


Journal = namedtuple("Journal", ["journalNm", "journalId"])
Tag = namedtuple("Tag", ["tagId", "tagName"])
