from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

from os import getenv
from dotenv import load_dotenv

load_dotenv()
DB_URL = getenv("DB_URL")
if DB_URL is None:
    raise ValueError("please define DB_URL in .env file first.")

class engineconn:
    def __init__(self) -> None:
        self.engine = create_engine(DB_URL, pool_recycle=500)
    

    def session_maker(self) -> sessionmaker:
        session_maker: sessionmaker = sessionmaker(bind=self.engine)
        session = session_maker()

        return session
    

    def connection(self):
        conn = self.engine.connect()

        return conn
