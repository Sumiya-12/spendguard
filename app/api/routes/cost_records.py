from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.cost_record import CostRecordCreate

router = APIRouter(prefix="/cost-records", tags=["Cost Records"])

# In-memory storage (temporary)
cost_records_db = []


@router.post("")
def create_cost_record(payload: CostRecordCreate):
    record = payload.model_dump()
    cost_records_db.append(record)

    return {
        "message": "Cost record stored successfully",
        "data": record
    }


@router.get("")
def get_cost_records(
    provider: Optional[str] = Query(None),
    environment: Optional[str] = Query(None)
):
    filtered_records = []

    for record in cost_records_db:
        provider_match = (
            provider is None or
            record["provider"].lower() == provider.lower()
        )

        environment_match = (
            environment is None or
            (record["environment"] and record["environment"].lower() == environment.lower())
        )

        if provider_match and environment_match:
            filtered_records.append(record)

    return {
        "count": len(filtered_records),
        "data": filtered_records
    }
