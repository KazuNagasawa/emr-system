from datetime import date
from pydantic import BaseModel

class PatientCreate(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    gender: str | None = None

class PatientResponse(BaseModel):
    id: int
    last_name: str
    first_name: str
    birth_date: date
    gender: str | None = None

    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic 変換用
