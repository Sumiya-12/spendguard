from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.services.cost_record_service import get_cost_record_by_id, delete_cost_record_by_id, create_cost_record, update_cost_record_by_id, get_cost_records
from app.schemas.cost_record import CostRecordCreate, CostRecordUpdate, CostRecordResponse, CostRecordListResponse
from app.schemas.cost_record import ProviderEnum, EnvironmentEnum
from app.models.cost_record import CostRecord
from app.core.database import get_db

router = APIRouter(prefix="/cost-records", tags=["Cost Records"])


@router.post("/", response_model=CostRecordResponse)
def create_cost_record_route(payload: CostRecordCreate, db: Session = Depends(get_db)):
    record = create_cost_record(db, payload)

    return record


@router.get("/", response_model=CostRecordListResponse)
def get_cost_records_route(
    provider: Optional[ProviderEnum] = Query(None),
    environment: Optional[EnvironmentEnum] = Query(None),
    sort_by: str = Query("usage_date"),
    order: str = Query("desc"),
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):

    return get_cost_records(db, provider, environment, sort_by, order, limit, offset)

@router.get("/total-cost")
def get_total_cost(
    provider: Optional[str] = Query(None),
    environment: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(func.sum(CostRecord.cost_amount))

    if provider is not None:
        query = query.filter(CostRecord.provider.ilike(provider))

    if environment is not None:
        query = query.filter(CostRecord.environment.ilike(environment))

    total_cost = query.scalar()

    if total_cost is None:
        total_cost = 0.0
    return {
        "provider_filter": provider,
        "environment_filter": environment,
        "total_cost": total_cost,
        "currency": "USD"
    }

@router.get("/{record_id}", response_model=CostRecordResponse)
def get_cost_record_by_id_route(record_id: int, db: Session = Depends(get_db)):
    record = get_cost_record_by_id(db, record_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Cost record not found")

    return record

@router.delete("/{record_id}", status_code=204)
def delete_cost_record(record_id: int, db: Session = Depends(get_db)):
    record= delete_cost_record_by_id(db, record_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Cost record not found")


@router.patch("/{record_id}", response_model=CostRecordResponse)
def update_cost_record(
    record_id: int,
    payload: CostRecordUpdate,
    db: Session = Depends(get_db)
):

    record = update_cost_record_by_id(db, record_id, payload)

    if record is None:
        raise HTTPException(status_code=404, detail="Cost record not found")

    return record
