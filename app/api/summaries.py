from fastapi import APIRouter, HTTPException
from typing import List

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema


router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema):
    summary_id = await crud.post(payload)
    return {"id": summary_id, "url": payload.url}


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int):
    summary = await crud.get(id)

    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries():
    return await crud.get_all()