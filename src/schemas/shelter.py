from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ShelterBase(BaseModel):
    name: str
    address: str


class ShelterCreate(ShelterBase):
    pass


class ShelterResponse(ShelterBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)