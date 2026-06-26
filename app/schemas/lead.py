"""线索Schema"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class LeadCreate(BaseModel):
    """创建线索请求"""
    employer_name: Optional[str] = None
    employer_phone: str
    employer_wechat: Optional[str] = None

    service_type: str = Field(..., description="服务类型：育儿嫂/月嫂/保洁")
    service_form: Optional[str] = Field(None, description="住家/白班/钟点")
    city: str
    district: Optional[str] = None
    address: Optional[str] = None

    family_size: Optional[int] = None
    has_pet: int = 0
    baby_age: Optional[int] = None
    elderly_count: int = 0

    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    expect_date: Optional[datetime] = None
    urgency: int = 0

    preference: Optional[Dict] = {}
    source: str = "miniprogram"


class LeadResponse(BaseModel):
    """线索响应"""
    id: int
    employer_name: Optional[str]
    employer_phone: str
    service_type: str
    city: str
    district: Optional[str]
    budget_min: Optional[int]
    budget_max: Optional[int]
    ai_score: float
    ai_level: str
    ai_reason: Optional[str]
    status: int
    created_at: datetime

    class Config:
        from_attributes = True


class LeadScoreResult(BaseModel):
    """线索评分结果"""
    score: float = Field(..., ge=0, le=100)
    level: str
    reason: str
    features: Dict
