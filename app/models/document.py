from app.models.base import BaseEntity

from sqlalchemy import DATE, Column, BIGINT, TEXT


class Document(BaseEntity):
    '''
    Website entity class
    (inherited from base entity)
    - id: BIGINT, NOT NULL, AUTO_INCREMENT, PK
    - created_at: DATE, NOT NULL, DEFAULT=date.today()
    - updated_at: DATE, NULL
    (end of inherited columns)

    - title: TEXT, NOT NULL, DEFAULT="제목 없음"
    - content: TEXT, NOT NULL, DEFAULT="내용 없음"

    '''

    __tablename__ = "document"

    title = Column(
        TEXT,
        nullable=False,
        default="제목 없음",
    )

    content = Column(
        TEXT,
        nullable=False,
        default="내용 없음",
    )
