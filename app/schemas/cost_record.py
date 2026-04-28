from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class ProviderEnum(str, Enum):
    aws = "aws"
    azure = "azure"
    gcp = "gcp"

class EnvironmentEnum(str, Enum):
    dev = "dev"
    qa = "qa"
    prod = "prod"

class CostRecordCreate(BaseModel):
    provider: ProviderEnum
    account_name: str
    service_name: str
    resource_id: str
    environment: EnvironmentEnum
    owner: str
    cost_amount: float = Field(..., gt=0)
    currency: str
    usage_date: date

class CostRecordUpdate(BaseModel):
    provider: Optional[ProviderEnum] = None
    account_name: Optional[str] = None
    service_name: Optional[str] = None
    resource_id: Optional[str] = None
    environment: Optional[EnvironmentEnum] = None
    owner: Optional[str] = None
    cost_amount: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = None
    usage_date: Optional[date] = None

class CostRecordResponse(BaseModel):
    id: int
    provider: ProviderEnum
    account_name: str
    service_name: str
    environment: EnvironmentEnum
    owner: str
    cost_amount: float
    currency: str
    usage_date: date

    class Config:
        from_attributes = True

class CostRecordListResponse(BaseModel):
    count: int
    sort_by: str
    order: str
    limit: int
    offset: int
    data: List[CostRecordResponse]
