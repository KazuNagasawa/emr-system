import uuid
from datetime import datetime, date
from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Encounter(Base):
    __tablename__ = "encounters"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    encounter_date: Mapped[date] = mapped_column(Date, nullable=False)

    encounter_type: Mapped[str] = mapped_column(String(50), nullable=False)  
    # 例: "outpatient", "inpatient", "emergency"

    department: Mapped[str | None] = mapped_column(String(100))
    physician_name: Mapped[str | None] = mapped_column(String(100))

    chief_complaint: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 🔗 Patientとのリレーション
    patient = relationship("Patient", back_populates="encounters")
