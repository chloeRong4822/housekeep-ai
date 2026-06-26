"""家政公司Schema"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str
    contact_name: Optional[str] = None
    phone: str
    email: Optional[str] = None
    service_areas: List[str] = []
    service_types: List[str] = []


class CompanyResponse(BaseModel):
    id: int
    name: str
    contact_name: Optional[str]
    phone: str
    service_areas: List[str]
    service_types: List[str]
    credit_score: float
    completion_rate: float
    total_orders: int
    vip_level: int
    status: int
    created_at: datetime

    class Config:
        from_attributes = True
