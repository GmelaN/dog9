from dataclasses import dataclass

@dataclass
class DocumentDTO:
    title: str
    content: str
    type: str
    category: str
    href: str
