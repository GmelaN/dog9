from collections import namedtuple

News = namedtuple("News", ["title", "content", "url", "pub_time", "tag", "press", "image"])
Article = namedtuple("Article", ["title", "content", "url", "pub_time", "tag", "press", "problem", "issue", "keyword"])
SummerizedNews = namedtuple("SummerizedNews", ["title", "content", "topics", "id"])


Journal = namedtuple("Journal", ["journalNm", "journalId"])

Tag = namedtuple("Tag", ["tagId", "tagName"])
