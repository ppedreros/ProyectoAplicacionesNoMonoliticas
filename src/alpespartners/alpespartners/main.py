from fastapi import FastAPI
import uvicorn
from alpespartners.api.tracking import router as tracking_router

from alpespartners.api.tracking import router as tracking_router
from alpespartners.api.loyalty import router as loyalty_router

# Crear instancia de FastAPI
app = FastAPI(
    title="Alpes Partners - Tracking Service",
    description="Servicio de tracking para Alpes Partners"
)

# Registrar rutas
app.include_router(tracking_router, prefix="/v1", tags=["tracking"])
app.include_router(loyalty_router, prefix="/v1", tags=["loyalty"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": ["tracking", "loyalty"],
        "message": "Alpes Partners microservices POC"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)