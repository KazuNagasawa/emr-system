from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class PatientCreate(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    gender: str | None = None


class PatientResponse(BaseModel):
    id: UUID
    last_name: str
    first_name: str
    birth_date: date
    gender: str | None = None

    model_config = ConfigDict(from_attributes=True)
