"""
FastAPI Backend for No Colon, Still Rollin'
Medical-grade anti-cancer food protocol system
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="No Colon Still Rollin API",
    description="Anti-cancer food protocol generator with keto compatibility and research-backed dosing",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database and seed data on startup"""
    try:
        logger.info("Starting application initialization...")

        # Import here to avoid circular dependencies
        from app.core.database import Database
        from app.core.init_database import seed_foods, create_jesse_user

        # Initialize database (creates tables if they don't exist)
        db = Database()
        logger.info("Database connection established")

        # Check if database needs seeding (check if foods table is empty)
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM foods")
        food_count = cursor.fetchone()[0]

        if food_count == 0:
            logger.info("Database is empty. Seeding initial data...")
            seed_foods(db)
            create_jesse_user(db)
            logger.info("Database seeding complete")
        else:
            logger.info(f"Database already contains {food_count} foods")

        db.close()
        logger.info("Application initialization complete")

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        # Don't fail startup - allow the app to run even if seeding fails
        # The database tables will still be created

# CORS middleware - allow development and Replit domains
origins_env = os.getenv("CORS_ORIGINS", "")
if origins_env:
    origins = origins_env.split(",")
else:
    # Default: local development + Replit domains
    origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.replit.dev",
        "https://*.replit.app",
        "https://*.repl.co"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.replit\.(dev|app|co)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
from app.api import protocol, weight, compliance, foods, status, library, exports, health_photos, medications, hydration

app.include_router(protocol.router, prefix="/api/protocol", tags=["Protocol"])
app.include_router(weight.router, prefix="/api/weight", tags=["Weight"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(foods.router, prefix="/api/foods", tags=["Foods"])
app.include_router(status.router, prefix="/api/status", tags=["Status"])
app.include_router(library.router, prefix="/api/library", tags=["Library"])
app.include_router(exports.router, prefix="/api/exports", tags=["Exports"])
app.include_router(health_photos.router, prefix="/api/health-photos", tags=["Health Photos"])
app.include_router(medications.router, prefix="/api/medications", tags=["Medications"])
app.include_router(hydration.router, prefix="/api/hydration", tags=["Hydration"])

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "message": "No Colon, Still Rollin'"
    }

# Root endpoint - useful when frontend isn't built yet
@app.get("/")
def root():
    """Root endpoint that redirects to docs or shows status"""
    frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"

    if not frontend_dist.exists():
        return {
            "message": "No Colon, Still Rollin' API",
            "version": "2.0.0",
            "status": "Backend is running",
            "frontend": "Not built - run 'cd frontend && npm install && npm run build'",
            "endpoints": {
                "health": "/health",
                "api_docs": "/api/docs",
                "redoc": "/api/redoc"
            },
            "note": "Frontend should be built during deployment. If you're seeing this in production, the build step may have failed."
        }

    # If frontend is built, this won't be reached (static files will be served instead)
    return {
        "message": "No Colon, Still Rollin'",
        "version": "2.0.0"
    }

# Serve frontend static files in production
frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    logger.info(f"Mounting frontend static files from {frontend_dist}")
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")
else:
    logger.warning(f"Frontend dist directory not found at {frontend_dist}. Serving API only.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
