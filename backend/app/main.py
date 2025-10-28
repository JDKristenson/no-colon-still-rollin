"""
FastAPI Backend for No Colon, Still Rollin'
Medical-grade anti-cancer food protocol system
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

# Create FastAPI app
app = FastAPI(
    title="No Colon Still Rollin API",
    description="Anti-cancer food protocol generator with keto compatibility and research-backed dosing",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware for development
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
from app.api import protocol, weight, compliance, foods, status

app.include_router(protocol.router, prefix="/api/protocol", tags=["Protocol"])
app.include_router(weight.router, prefix="/api/weight", tags=["Weight"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(foods.router, prefix="/api/foods", tags=["Foods"])
app.include_router(status.router, prefix="/api/status", tags=["Status"])

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "message": "No Colon, Still Rollin'"
    }

# Serve frontend static files in production
frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
