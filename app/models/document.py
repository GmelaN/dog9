from app.models.base import BaseEntity

from sqlalchemy import Column, BIGINT, TEXT, ForeignKey
from sqlalchemy.orm import relationship

class Document(BaseEntity):
    '''
    ## website document entity class
    ### inherited from base entity
    - id: BIGINT, NOT NULL, AUTO_INCREMENT, PK
    - created_at: DATE, NOT NULL, DEFAULT=date.today()
    - updated_at: DATE, NULL
    
    ### columns
    - title: TEXT, NOT NULL, DEFAULT="제목 없음"
    - content: TEXT, NOT NULL, DEFAULT="내용 없음"

    ### columns with relationship
    - source_type: relationship(SourceType)
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

    # 역방향 관계 설정
    source_type_id = Column(
        BIGINT,
        ForeignKey('source_type.id')
    )

    source_type = relationship("SourceType", back_populates="document")
