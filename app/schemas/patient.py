from pydantic import BaseModel, constr, Field
from typing import Optional, List
from datetime import date, datetime
from app.models.patient import Gender, BloodGroup

class HealthMetricBase(BaseModel):
    weight: float = Field(gt=0)
    bmi: Optional[float] = Field(None, gt=0)
    blood_pressure: Optional[str] = None
    blood_sugar: Optional[float] = None
    notes: Optional[str] = None

class HealthMetricCreate(HealthMetricBase):
    date: date

class HealthMetricResponse(HealthMetricBase):
    id: int
    patient_id: int
    date: date

    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    date_of_birth: date
    gender: Gender
    blood_group: BloodGroup
    height: float = Field(gt=0)
    weight: float = Field(gt=0)
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    activity_level: str
    food_preferences: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    emergency_contact_name: str
    emergency_contact_phone: str
    emergency_contact_relation: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    height: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    activity_level: Optional[str] = None
    food_preferences: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    user_id: int
    created_at: datetime
    health_metrics: List[HealthMetricResponse] = []

    class Config:
        from_attributes = True 