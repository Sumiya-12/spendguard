from pydantic import BaseModel
from datetime import date
from typing import Optional

class CostRecordCreate(BaseModel):
    provider: str
    account_name: str
    service_name: str
    resource_id: str
    environment: Optional[str] = None
    owner: Optional[str] = None
    cost_amount: float
    currency: str
    usage_date: date
