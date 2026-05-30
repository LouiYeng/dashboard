"""
FastAPI application entry point.

Mounts all routers, configures CORS, and provides
startup/shutdown lifecycle hooks for database initialization.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.auth.router import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.sales import router as sales_router
from app.routers.branches import router as branches_router
from app.routers.exports import router as exports_router
from app.routers.users import router as users_router
from app.routers.inventory import router as inventory_router
from app.routers.purchases import router as purchases_router
from app.routers.expenses import router as expenses_router

settings = get_settings()


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Business Intelligence Dashboard API for POS data analytics",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount routers under /api/v1
    api_prefix = "/api/v1"
    app.include_router(auth_router, prefix=api_prefix)
    app.include_router(dashboard_router, prefix=api_prefix)
    app.include_router(sales_router, prefix=api_prefix)
    app.include_router(branches_router, prefix=api_prefix)
    app.include_router(exports_router, prefix=api_prefix)
    app.include_router(users_router, prefix=api_prefix)
    app.include_router(inventory_router, prefix=api_prefix)
    app.include_router(purchases_router, prefix=api_prefix)
    app.include_router(expenses_router, prefix=api_prefix)

    # Startup event: create dashboard tables and seed admin
    @app.on_event("startup")
    def on_startup():
        from app.services.migration_service import create_dashboard_tables, seed_admin_user
        from app.database import SessionLocal
        try:
            create_dashboard_tables()
            db = SessionLocal()
            try:
                result = seed_admin_user(db)
                if result.get("created"):
                    print(f"[STARTUP] {result['message']}")
            finally:
                db.close()
        except Exception as e:
            print(f"[STARTUP WARNING] Could not initialize dashboard tables: {e}")

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc) if settings.DEBUG else "Internal server error"},
        )

    # Health check
    @app.get("/api/health")
    def health_check():
        return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}

    # Seed endpoint (for initial setup)
    @app.post("/api/v1/seed")
    def seed_data():
        """Seed sample data for testing. Remove in production."""
        from app.services.migration_service import seed_all
        from app.database import SessionLocal
        db = SessionLocal()
        try:
            result = seed_all(db)
            return {"message": "Seed complete", "results": result}
        finally:
            db.close()

    return app


app = create_app()
