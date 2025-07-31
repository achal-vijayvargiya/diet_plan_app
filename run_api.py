import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Get the absolute path to the API directory
    BASE_DIR = Path(__file__).resolve().parent
    api_path = os.path.join(BASE_DIR, "app", "api", "main.py")
    
    # Run the FastAPI server
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    ) 