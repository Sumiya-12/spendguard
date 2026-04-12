from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.cost_record import CostRecordCreate
from app.models.cost_record import CostRecord
from app.core.database import get_db

router = APIRouter(prefix="/cost-records", tags=["Cost Records"])


@router.post("")
def create_cost_record(payload: CostRecordCreate, db: Session = Depends(get_db)):
    record = CostRecord(
        provider=payload.provider,
        account_name=payload.account_name,
        service_name=payload.service_name,
        resource_id=payload.resource_id,
        environment=payload.environment,
        owner=payload.owner,
        cost_amount=payload.cost_amount,
        currency=payload.currency,
        usage_date=payload.usage_date,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "message": "Cost record stored successfully",
        "data": {
            "id": record.id,
            "provider": record.provider,
            "account_name": record.account_name,
            "service_name": record.service_name,
            "resource_id": record.resource_id,
            "environment": record.environment,
            "owner": record.owner,
            "cost_amount": record.cost_amount,
            "currency": record.currency,
            "usage_date": str(record.usage_date),
        }
    }


@router.get("")
def get_cost_records(
    provider: Optional[str] = Query(None),
    environment: Optional[str] = Query(None),
    sort_by: str = Query("usage_date"),
    order: str = Query("desc"),
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    query = db.query(CostRecord)

    if provider is not None:
        query = query.filter(CostRecord.provider.ilike(provider))

    if environment is not None:
        query = query.filter(CostRecord.environment.ilike(environment))

    allowed_sort_fields = {
        "id": CostRecord.id,
        "provider": CostRecord.provider,
        "environment": CostRecord.environment,
        "cost_amount": CostRecord.cost_amount,
        "usage_date": CostRecord.usage_date,
    }

    sort_column = allowed_sort_fields.get(sort_by, CostRecord.usage_date)

    if order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    query = query.limit(limit).offset(offset)

    records = query.all()

    data = []
    for record in records:
        data.append({
            "id": record.id,
            "provider": record.provider,
            "account_name": record.account_name,
            "service_name": record.service_name,
            "resource_id": record.resource_id,
            "environment": record.environment,
            "owner": record.owner,
            "cost_amount": record.cost_amount,
            "currency": record.currency,
            "usage_date": str(record.usage_date),
        })

    return {
        "count": len(data),
        "sort_by": sort_by,
        "order": order,
        "limit": limit,
        "offset": offset,
        "data": data
    }

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

@router.get("/{record_id}")
def get_cost_record_by_id(record_id: int, db: Session = Depends(get_db)):
    record = db.query(CostRecord).filter(CostRecord.id == record_id).first()

    if record is None:
        raise HTTPException(status_code=404, detail="Cost record not found")

    return {
        "id": record.id,
        "provider": record.provider,
        "account_name": record.account_name,
        "service_name": record.service_name,
        "resource_id": record.resource_id,
        "environment": record.environment,
        "owner": record.owner,
        "cost_amount": record.cost_amount,
        "currency": record.currency,
        "usage_date": str(record.usage_date),
    }
