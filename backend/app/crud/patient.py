from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from uuid import UUID



async def create_patient(db: AsyncSession, patient: PatientCreate):
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient


async def get_patients(db: AsyncSession):
    result = await db.execute(select(Patient).order_by(Patient.id))
    return result.scalars().all()


async def get_patient(db: AsyncSession, patient_id):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    return result.scalar_one_or_none()

async def update_patient(db: AsyncSession, patient_id: UUID, patient: PatientUpdate):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    db_patient = result.scalar_one_or_none()

    if not db_patient:
        return None

    for key, value in patient.model_dump(exclude_unset=True).items():
        setattr(db_patient, key, value)

    await db.commit()
    await db.refresh(db_patient)
    return db_patient


async def delete_patient(db: AsyncSession, patient_id: UUID) -> bool:
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    db_patient = result.scalar_one_or_none()

    if not db_patient:
        return False

    await db.delete(db_patient)
    await db.commit()
    return True

