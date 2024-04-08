from dataclasses import dataclass

@dataclass
class Document:
    title: str
    content: str
    type: str
    category: str
    href: str
