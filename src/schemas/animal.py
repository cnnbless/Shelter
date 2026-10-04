from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AnimalBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    health_status: Optional[str] = None


class AnimalCreate(AnimalBase):
    shelter_id: int


class AnimalResponse(AnimalBase):
    id: int
    shelter_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)