from sqlalchemy import Column, Integer, String, Float, Date
from app.core.database import Base


class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    environment = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    cost_amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    usage_date = Column(Date, nullable=False)
