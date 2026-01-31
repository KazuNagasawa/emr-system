from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db import get_db
from app.schemas.patient import PatientCreate, PatientResponse,PatientUpdate
from app.crud.patient import create_patient, get_patients, get_patient
from app.crud.patient import update_patient, delete_patient,update_patient


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

@router.put("/{patient_id}", response_model=PatientResponse)
async def update(patient_id: UUID, patient: PatientUpdate, db: AsyncSession = Depends(get_db)):
    updated = await update_patient(db, patient_id, patient)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated

@router.delete("/{patient_id}", status_code=204)
async def delete(patient_id: UUID, db: AsyncSession = Depends(get_db)):
    deleted = await delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")

@router.patch("/{patient_id}", response_model=PatientResponse)
async def update_partial(
    patient_id: UUID,
    patient: PatientUpdate,
    db: AsyncSession = Depends(get_db),
):
    updated_patient = await update_patient(db, patient_id, patient)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient
