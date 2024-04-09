from dataclasses import asdict
from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.services.fetcher import fetch_feed
from app.models.document import Document

router = APIRouter()

@router.get("/feeds/all", response_model=List[Dict])
async def get_filtered_feed():

    try:
        documents = await fetch_feed()
        result = [asdict(document) for document in documents]
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
