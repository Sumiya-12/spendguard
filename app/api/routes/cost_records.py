from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.cost_record import CostRecordCreate

router = APIRouter(prefix="/cost-records", tags=["Cost Records"])

# In-memory storage (temporary)
cost_records_db = []


@router.post("")
def create_cost_record(payload: CostRecordCreate):
    record = payload.model_dump()

    # store the record
    cost_records_db.append(record)

    return {
        "message": "Cost record stored successfully",
        "data": record
    }


@router.get("")
def get_cost_records(provider: Optional[str] = Query(None)):
    if provider is None:
        return {
            "count": len(cost_records_db),
            "data": cost_records_db
        }

    filtered_records = []

    for record in cost_records_db:
        if record["provider"].lower() == provider.lower():
            filtered_records.append(record)

    return {
        "count": len(filtered_records),
        "data": filtered_records
    }
