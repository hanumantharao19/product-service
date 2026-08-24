from fastapi import FastAPI
from sqlalchemy import text

from .database import Base, engine
from .routes.products import router as product_router


app = FastAPI(
    title="E-Commerce Product Service",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


app.include_router(product_router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "product-service"
    }


@app.get("/ready")
def readiness():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ready",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "not ready",
            "database": "unavailable"
        }


