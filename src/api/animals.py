from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from src.models.entities import Animal
from src.schemas.animal import AnimalCreate, AnimalResponse
from src.api.dependencies import get_db

router = APIRouter(prefix="/animals", tags=["animals"])


@router.post("/", response_model=AnimalResponse)
async def create_animal(animal_in: AnimalCreate, db: AsyncSession = Depends(get_db)):
    new_animal = Animal(**animal_in.model_dump())
    db.add(new_animal)
    await db.commit()
    await db.refresh(new_animal)
    return new_animal


@router.get("/", response_model=List[AnimalResponse])
async def get_animals(
        species: Optional[str] = Query(None, description="Фільтр за видом"),
        breed: Optional[str] = Query(None, description="Фільтр за породою"),
        min_age: Optional[int] = Query(None, description="Мінімальний вік"),
        max_age: Optional[int] = Query(None, description="Максимальний вік"),
        db: AsyncSession = Depends(get_db)
):
    query = select(Animal)

    # Динамічна побудова запиту на основі переданих параметрів
    if species:
        query = query.where(Animal.species.ilike(f"%{species}%"))
    if breed:
        query = query.where(Animal.breed.ilike(f"%{breed}%"))
    if min_age is not None:
        query = query.where(Animal.age >= min_age)
    if max_age is not None:
        query = query.where(Animal.age <= max_age)

    result = await db.execute(query)
    return result.scalars().all()