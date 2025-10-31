from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title="No Colon, Still Rollin' API",
    description="Integrated Cancer Protocol & Workout System",
    version="3.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "No Colon, Still Rollin' API", "version": "3.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

