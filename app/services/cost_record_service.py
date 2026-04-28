from sqlalchemy.orm import Session
from typing import Optional
from app.models.cost_record import CostRecord
from app.schemas.cost_record import CostRecordCreate, CostRecordUpdate, ProviderEnum, EnvironmentEnum

def get_cost_record_by_id(db: Session, record_id: int):
    return db.query(CostRecord).filter(CostRecord.id == record_id).first()

def delete_cost_record_by_id(db: Session, record_id: int):
    record = get_cost_record_by_id(db,record_id)
    if record is None:
        return None
   
    db.delete(record)
    db.commit()

    return record

def create_cost_record(db: Session, payload: CostRecordCreate):
    record = CostRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record	

def update_cost_record_by_id(db: Session, record_id: int, payload: CostRecordUpdate):
    record = get_cost_record_by_id(db, record_id)

    if record is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record

def get_cost_records(
    db: Session,
    provider: Optional[ProviderEnum],
    environment: Optional[EnvironmentEnum],
    sort_by: str,
    order: str,
    limit: int,
    offset: int,
):
    query = db.query(CostRecord)

    if provider:
        query = query.filter(CostRecord.provider == provider)

    if environment:
        query = query.filter(CostRecord.environment == environment)

    if sort_by == "cost_amount":
        sort_column = CostRecord.cost_amount
    else:
        sort_column = CostRecord.usage_date

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    total = query.count()

    records = query.limit(limit).offset(offset).all()

    return {
        "count": total,
        "sort_by": sort_by,
        "order": order,
        "limit": limit,
        "offset": offset,
        "data": records,
    }
