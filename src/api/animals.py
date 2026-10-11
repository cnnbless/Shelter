import os
import shutil

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.dependencies import get_db, require_admin
from src.models.entities import Animal
from src.schemas.animal import AnimalCreate, AnimalResponse

router = APIRouter(prefix="/animals", tags=["animals"])


@router.post("/", response_model=AnimalResponse, dependencies=[Depends(require_admin)])
async def create_animal(animal_in: AnimalCreate, db: AsyncSession = Depends(get_db)):
    new_animal = Animal(**animal_in.model_dump())
    db.add(new_animal)
    await db.commit()
    await db.refresh(new_animal)
    return new_animal


@router.post("/{animal_id}/upload-media", dependencies=[Depends(require_admin)])
async def upload_animal_media(animal_id: int, file: UploadFile = File(...)):
    os.makedirs("media", exist_ok=True)
    file_path = f"media/animal_{animal_id}_{file.filename}"

    try:
        with open(file_path, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write file: {e!s}")

    return {
        "file_path": file_path,
        "media_url": f"/media/animal_{animal_id}_{file.filename}",
    }


@router.get("/", response_model=list[AnimalResponse])
async def get_animals(
    species: str | None = Query(None),
    breed: str | None = Query(None),
    min_age: int | None = Query(None),
    max_age: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Animal)
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
