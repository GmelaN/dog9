from app.models.base import Base

from sqlalchemy import Column, TEXT, Integer, ForeignKey
from sqlalchemy.orm import relationship


class SourceType(Base):
    '''
    ## website source type entity class
    ### inherited from base entity
    - id: BIGINT, NOT NULL, AUTO_INCREMENT, PK
    - created_at: DATE, NOT NULL, DEFAULT=date.today()
    - updated_at: DATE, NULL
    
    ### columns
    - name: TEXT, NOT NULL, DEFAULT="분류 없음"

    ### columns with relationship
    - websites: relationship(SourceType)
    - document: relationship(SourceType)
    '''
    
    __tablename__ = "source_type"

    name = Column(TEXT, nullable=False, default="분류 없음")

    # 역방향 관계 정의
    websites = relationship("Website", back_populates="source_type")
    document = relationship("Document", back_populates="source_type")
