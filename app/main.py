from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.base import engine, Base
from app.routers import users, doctors, patients

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Diet Planner API",
    description="API for managing diet plans and users",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(doctors.router)
app.include_router(patients.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Diet Planner API v2",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 