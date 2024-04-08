from fastapi import FastAPI
from app.routers import feed

app = FastAPI()

app.include_router(feed.router)
