from fastapi import APIRouter
from app.api.v1.endpoints import auth, dashboard, protocol, workouts, soreness, compliance

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(protocol.router, prefix="/protocol", tags=["protocol"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(soreness.router, prefix="/soreness", tags=["soreness"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])

