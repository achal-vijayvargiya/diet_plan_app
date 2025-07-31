from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base
from .user import User

# Association table for doctor-patient relationship
doctor_patient = Table(
    'doctor_patient',
    Base.metadata,
    Column('doctor_id', Integer, ForeignKey('doctors.id')),
    Column('patient_id', Integer, ForeignKey('patients.id'))
)

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    specialization = Column(String)
    license_number = Column(String, unique=True)
    years_of_experience = Column(Integer)
    consultation_fee = Column(Integer)
    available_hours = Column(String)  # JSON string of availability schedule
    
    # Relationships
    user = relationship("User", backref="doctor_profile", uselist=False)
    patients = relationship("Patient", secondary=doctor_patient, back_populates="doctors")
    created_diet_plans = relationship("DietPlan", back_populates="created_by")

    def __repr__(self):
        return f"<Doctor {self.user.username}>" 