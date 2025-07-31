from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class DoctorBase(BaseModel):
    specialization: str
    license_number: constr(min_length=5)
    years_of_experience: int
    consultation_fee: int
    available_hours: str

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    consultation_fee: Optional[int] = None
    available_hours: Optional[str] = None

class DoctorResponse(DoctorBase):
    id: int
    user_id: int
    created_at: datetime
    patient_count: Optional[int] = None

    class Config:
        from_attributes = True 