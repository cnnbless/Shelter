from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ShelterBase(BaseModel):
    name: str
    address: str


class ShelterCreate(ShelterBase):
    pass


class ShelterResponse(ShelterBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
