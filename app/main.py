from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.cost_records import router as cost_records_router

app = FastAPI(title="SpendGuard API", version="0.1.0")

app.include_router(health_router)
app.include_router(cost_records_router)


@app.get("/")
def root():
    return {"message": "SpendGuard API is running"}
