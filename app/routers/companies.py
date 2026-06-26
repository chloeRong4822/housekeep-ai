"""家政公司路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse
from app.models.company import Company

router = APIRouter(prefix="/api/v1/housekeeping/companies", tags=["家政公司"])


@router.post("/create", response_model=CompanyResponse)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    """创建家政公司"""
    company = Company(
        name=data.name,
        contact_name=data.contact_name,
        phone=data.phone,
        email=data.email,
        service_areas=data.service_areas,
        service_types=data.service_types,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("/list", response_model=List[CompanyResponse])
def list_companies(
    city: str = None,
    service_type: str = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """获取家政公司列表"""
    query = db.query(Company).filter(Company.status == 1)
    # 简化：不按区域过滤
    if service_type:
        query = query.filter(Company.service_types.contains([service_type]))

    companies = query.order_by(Company.credit_score.desc()).offset(offset).limit(limit).all()
    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """获取公司详情"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="公司不存在")
    return company


@router.post("/{company_id}/recharge")
def recharge(company_id: int, amount: float, db: Session = Depends(get_db)):
    """账户充值"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="公司不存在")
    company.balance += amount
    db.commit()
    return {"company_id": company_id, "balance": company.balance}
