import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from api import router as api_router
from config import API_PREFIX, ALLOW_ORIGINS, UPLOAD_DIR

# Create directory structure if it doesn't exist
os.makedirs("tmp/lancedb", exist_ok=True)
os.makedirs("knowledge", exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="P-Bot API",
    description="API for the P-Bot real estate chatbot with multiple specialized agents",
    version="0.2.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Include API router
app.include_router(api_router, prefix=API_PREFIX)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok", 
        "message": "P-Bot API is running",
        "version": "0.2.0",
        "features": ["multi-agent", "image-processing", "tenancy-faq"]
    }

# Load some initial tenancy knowledge if available
try:
    from utils.knowledge_loader import load_initial_knowledge
    load_initial_knowledge()
except Exception as e:
    print(f"Warning: Failed to load initial knowledge: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True) 