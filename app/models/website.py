from app.models.base import BaseEntity

from sqlalchemy import Column, TEXT


class Website(BaseEntity):
    '''
    Website entity class
    (inherited from base entity)
    - id: BIGINT, NOT NULL, AUTO_INCREMENT, PK
    - created_at: DATE, NOT NULL, DEFAULT=date.today()
    - updated_at: DATE, NULL
    (end of inherited columns)

    - name: TEXT, NOT NULL, DEFAULT="제목 없음"
    - url: TEXT, NOT NULL

    '''

    __tablename__ = "website"
    
    name = Column(
        TEXT,
        nullable=False,
        default="제목 없음"
    )

    url = Column(
        TEXT,
        nullable=False,
    )
