from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.dependencies import get_db, require_admin
from src.models.entities import Shelter
from src.schemas.shelter import ShelterCreate, ShelterResponse

router = APIRouter(prefix="/shelters", tags=["shelters"])


@router.post("/", response_model=ShelterResponse, dependencies=[Depends(require_admin)])
async def create_shelter(shelter_in: ShelterCreate, db: AsyncSession = Depends(get_db)):
    new_shelter = Shelter(**shelter_in.model_dump())
    db.add(new_shelter)
    await db.commit()
    await db.refresh(new_shelter)
    return new_shelter


@router.get("/", response_model=list[ShelterResponse])
async def get_shelters(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Shelter))
    return result.scalars().all()
