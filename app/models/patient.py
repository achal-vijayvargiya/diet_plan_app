from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base
from .doctor import doctor_patient

class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class BloodGroup(PyEnum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Personal Information
    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    blood_group = Column(Enum(BloodGroup))
    
    # Health Information
    height = Column(Float)  # in cm
    weight = Column(Float)  # in kg
    allergies = Column(String)  # JSON string of allergies
    medical_conditions = Column(String)  # JSON string of conditions
    medications = Column(String)  # JSON string of current medications
    
    # Lifestyle Information
    activity_level = Column(String)
    food_preferences = Column(String)  # JSON string of preferences
    dietary_restrictions = Column(String)  # JSON string of restrictions
    
    # Emergency Contact
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)
    emergency_contact_relation = Column(String)
    
    # Relationships
    user = relationship("User", backref="patient_profile", uselist=False)
    doctors = relationship("Doctor", secondary=doctor_patient, back_populates="patients")
    diet_plans = relationship("DietPlan", back_populates="patient")
    health_metrics = relationship("HealthMetric", back_populates="patient")

    def __repr__(self):
        return f"<Patient {self.user.username}>"

class HealthMetric(Base):
    __tablename__ = "health_metrics"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(Date)
    weight = Column(Float)
    bmi = Column(Float)
    blood_pressure = Column(String)  # Format: "systolic/diastolic"
    blood_sugar = Column(Float)
    notes = Column(String)

    patient = relationship("Patient", back_populates="health_metrics")

    def __repr__(self):
        return f"<HealthMetric for patient {self.patient_id} on {self.date}>" 