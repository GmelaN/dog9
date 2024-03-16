from datetime import date

from sqlalchemy import DATE, Column, BIGINT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseEntity(Base):
    '''
    base entity class
    - id: BIGINT, NOT NULL, AUTO_INCREMENT, PK
    - created_at: DATE, NOT NULL, DEFAULT=date.today()
    - updated_at: DATE, NULL
    '''

    __abstract__ = True

    id = Column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    created_at = Column(
        DATE,
        default=date.today(),
        nullable=False
    )

    updated_at = Column(
        DATE,
        nullable=True
    )
