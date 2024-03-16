from app.models.base import BaseEntity

from sqlalchemy import Column, TEXT, ForeignKey, BIGINT
from sqlalchemy.orm import relationship

class Website(BaseEntity):
    '''
    ## website entity class
    ### inherited from base entity
    - id: BIGINT, NOT NULL, AUTO_INCREMENT, PK
    - created_at: DATE, NOT NULL, DEFAULT=date.today()
    - updated_at: DATE, NULL

    ### columns
    - name: TEXT, NOT NULL, DEFAULT="제목 없음"
    - url: TEXT, NOT NULL

    ### columns with relationship
    - source_type: relationship(SourceType)
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

    # 역방향 관계 설정
    source_type_id = Column(
        BIGINT,
        ForeignKey('source_type.id')
    )

    source_type = relationship("SourceType", back_populates="website")
