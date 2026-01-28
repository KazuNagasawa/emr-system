from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db import get_db
from app.schemas.patient import PatientCreate, PatientResponse
from app.crud.patient import create_patient, get_patients, get_patient

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("", response_model=PatientResponse)
async def create(patient: PatientCreate, db: AsyncSession = Depends(get_db)):
    db_patient = await create_patient(db, patient)
    return db_patient


@router.get("", response_model=list[PatientResponse])
async def read_all(db: AsyncSession = Depends(get_db)):
    return await get_patients(db)


@router.get("/{patient_id}", response_model=PatientResponse)
async def read_one(patient_id: UUID, db: AsyncSession = Depends(get_db)):
    patient = await get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
