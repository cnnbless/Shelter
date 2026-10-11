from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnimalBase(BaseModel):
    name: str
    species: str
    breed: str | None = None
    age: int | None = None
    health_status: str | None = None


class AnimalCreate(AnimalBase):
    shelter_id: int


class AnimalResponse(AnimalBase):
    id: int
    shelter_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
