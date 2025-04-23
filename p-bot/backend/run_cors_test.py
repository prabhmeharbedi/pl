from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Add CORS middleware with the updated Vercel origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://loopot.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/agents")
async def agents():
    """Test endpoint for agents."""
    return {
        "agents": [
            {
                "id": "test_agent",
                "name": "Test Agent",
                "description": "This is a test agent to verify CORS configuration.",
                "capabilities": ["text_analysis"],
                "examples": ["This is a test example"]
            }
        ]
    }

@app.get("/api-status")
async def status():
    """Test endpoint for API status."""
    return {"status": "ok", "message": "CORS test API is working"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "message": "CORS test API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 