from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.models.entities import Shelter
from src.schemas.shelter import ShelterCreate, ShelterResponse
from src.api.dependencies import get_db

router = APIRouter(prefix="/shelters", tags=["shelters"])

@router.post("/", response_model=ShelterResponse)
async def create_shelter(shelter_in: ShelterCreate, db: AsyncSession = Depends(get_db)):
    new_shelter = Shelter(**shelter_in.model_dump())
    db.add(new_shelter)
    await db.commit()
    await db.refresh(new_shelter)
    return new_shelter

@router.get("/", response_model=List[ShelterResponse])
async def get_shelters(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Shelter))
    return result.scalars().all()