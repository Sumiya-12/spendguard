from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.cost_records import router as cost_records_router
from app.core.database import Base, engine
from app.models.cost_record import CostRecord

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpendGuard API", version="0.1.0")

app.include_router(health_router)
app.include_router(cost_records_router)


@app.get("/")
def root():
    return {"message": "SpendGuard API is running"}
