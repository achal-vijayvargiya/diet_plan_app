from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.models.base import get_db
from app.models.user import User, UserRole
from app.models.patient import Patient, HealthMetric
from app.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    HealthMetricCreate,
    HealthMetricResponse
)
from app.auth.utils import get_current_user, check_doctor_access

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientResponse)
async def create_patient_profile(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if the user is a patient
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients can create patient profiles"
        )
    
    # Check if patient profile already exists
    existing_profile = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient profile already exists"
        )
    
    # Create new patient profile
    patient = Patient(
        user_id=current_user.id,
        **patient_data.dict()
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

@router.get("/me", response_model=PatientResponse)
async def read_patient_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a patient"
        )
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    return patient

@router.get("/{patient_id}", response_model=PatientResponse)
async def read_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_doctor_access)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    return patient

@router.put("/me", response_model=PatientResponse)
async def update_patient_profile(
    patient_data: PatientUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a patient"
        )
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    # Update patient profile
    for key, value in patient_data.dict(exclude_unset=True).items():
        setattr(patient, key, value)
    
    db.commit()
    db.refresh(patient)
    return patient

@router.post("/me/health-metrics", response_model=HealthMetricResponse)
async def create_health_metric(
    metric_data: HealthMetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a patient"
        )
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    # Create new health metric
    metric = HealthMetric(
        patient_id=patient.id,
        **metric_data.dict()
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

@router.get("/me/health-metrics", response_model=List[HealthMetricResponse])
async def read_health_metrics(
    start_date: date = None,
    end_date: date = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a patient"
        )
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    # Query health metrics with optional date filtering
    query = db.query(HealthMetric).filter(HealthMetric.patient_id == patient.id)
    if start_date:
        query = query.filter(HealthMetric.date >= start_date)
    if end_date:
        query = query.filter(HealthMetric.date <= end_date)
    
    metrics = query.order_by(HealthMetric.date.desc()).all()
    return metrics 