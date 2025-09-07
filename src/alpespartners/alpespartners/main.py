from fastapi import FastAPI
import uvicorn
from alpespartners.api.tracking import router as tracking_router

# Crear instancia de FastAPI
app = FastAPI(
    title="Alpes Partners - Tracking Service",
    description="Servicio de tracking para Alpes Partners"
)

# Registrar rutas
app.include_router(tracking_router, prefix="/v1", tags=["tracking"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)