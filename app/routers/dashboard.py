"""数据看板路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models.lead import Lead, LeadDispatch
from app.models.company import Company

router = APIRouter(prefix="/api/v1/housekeeping/dashboard", tags=["数据看板"])


@router.get("/overview")
def dashboard_overview(db: Session = Depends(get_db)):
    """平台总览"""
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)

    total_leads = db.query(Lead).count()
    today_leads = db.query(Lead).filter(func.date(Lead.created_at) == today).count()
    week_leads = db.query(Lead).filter(func.date(Lead.created_at) >= week_ago).count()

    total_companies = db.query(Company).filter(Company.status == 1).count()
    total_deals = db.query(Lead).filter(Lead.status == 2).count()

    # 平均AI评分
    avg_score = db.query(func.avg(Lead.ai_score)).scalar() or 0

    return {
        "total_leads": total_leads,
        "today_leads": today_leads,
        "week_leads": week_leads,
        "total_companies": total_companies,
        "total_deals": total_deals,
        "avg_ai_score": round(float(avg_score), 1),
        "conversion_rate": round(total_deals / max(total_leads, 1) * 100, 1),
    }


@router.get("/leads/by-city")
def leads_by_city(db: Session = Depends(get_db)):
    """各城市线索分布"""
    result = db.query(
        Lead.city,
        func.count(Lead.id).label("count"),
        func.avg(Lead.ai_score).label("avg_score"),
    ).group_by(Lead.city).order_by(func.count(Lead.id).desc()).limit(10).all()

    return [
        {"city": r.city, "count": r.count, "avg_score": round(float(r.avg_score or 0), 1)}
        for r in result
    ]


@router.get("/leads/by-type")
def leads_by_type(db: Session = Depends(get_db)):
    """各服务类型线索分布"""
    result = db.query(
        Lead.service_type,
        func.count(Lead.id).label("count"),
    ).group_by(Lead.service_type).order_by(func.count(Lead.id).desc()).all()

    return [{"type": r.service_type, "count": r.count} for r in result]


@router.get("/companies/top")
def top_companies(db: Session = Depends(get_db)):
    """优质家政公司排行"""
    companies = db.query(Company).filter(Company.status == 1).order_by(
        Company.credit_score.desc()
    ).limit(10).all()

    return [
        {
            "id": c.id,
            "name": c.name,
            "credit_score": c.credit_score,
            "completion_rate": c.completion_rate,
            "total_orders": c.total_orders,
        }
        for c in companies
    ]
