"""线索路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.lead import LeadCreate, LeadResponse, LeadScoreResult
from app.services.lead_scoring import LeadScoringService
from app.services.lead_dispatch import LeadDispatchService
from app.models.lead import Lead, LeadDispatch as LeadDispatchModel

router = APIRouter(prefix="/api/v1/housekeeping/leads", tags=["线索"])


@router.post("/create", response_model=LeadResponse)
async def create_lead(data: LeadCreate, db: Session = Depends(get_db)):
    """创建新线索并自动评分"""
    # 1. AI评分
    scoring = LeadScoringService()
    score, level, reason, features = await scoring.score(data)

    # 2. 创建线索
    lead = Lead(
        employer_name=data.employer_name,
        employer_phone=data.employer_phone,
        employer_wechat=data.employer_wechat,
        service_type=data.service_type,
        service_form=data.service_form,
        city=data.city,
        district=data.district,
        address=data.address,
        family_size=data.family_size,
        has_pet=data.has_pet,
        baby_age=data.baby_age,
        elderly_count=data.elderly_count,
        budget_min=data.budget_min,
        budget_max=data.budget_max,
        expect_date=data.expect_date,
        urgency=data.urgency,
        preference=data.preference,
        source=data.source,
        ai_score=score,
        ai_level=level,
        ai_reason=reason,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    # 3. 智能分发（高分线索自动分发）
    if level in ["high", "medium"]:
        dispatch = LeadDispatchService()
        companies = await dispatch.dispatch(db, lead, max_companies=3)
        for c in companies:
            ld = LeadDispatchModel(
                lead_id=lead.id,
                company_id=c["company_id"],
                match_score=c["match_score"],
                match_reason=c["match_reason"],
                charge=c["charge"],
            )
            db.add(ld)
        db.commit()

    return lead


@router.post("/{lead_id}/score", response_model=LeadScoreResult)
async def score_lead(lead_id: int, db: Session = Depends(get_db)):
    """重新评分线索"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="线索不存在")

    data = LeadCreate(
        employer_name=lead.employer_name,
        employer_phone=lead.employer_phone,
        service_type=lead.service_type,
        city=lead.city,
        district=lead.district,
        budget_min=lead.budget_min,
        budget_max=lead.budget_max,
        urgency=lead.urgency,
        preference=lead.preference or {},
    )

    scoring = LeadScoringService()
    score, level, reason, features = await scoring.score(data)

    # 更新评分
    lead.ai_score = score
    lead.ai_level = level
    lead.ai_reason = reason
    db.commit()

    return LeadScoreResult(score=score, level=level, reason=reason, features=features)


@router.post("/{lead_id}/dispatch")
async def dispatch_lead(lead_id: int, db: Session = Depends(get_db)):
    """手动触发线索分发"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="线索不存在")

    dispatch = LeadDispatchService()
    companies = await dispatch.dispatch(db, lead, max_companies=5)

    # 保存分发记录
    for c in companies:
        ld = LeadDispatchModel(
            lead_id=lead.id,
            company_id=c["company_id"],
            match_score=c["match_score"],
            match_reason=c["match_reason"],
            charge=c["charge"],
        )
        db.add(ld)

    lead.status = 1
    db.commit()

    return {"lead_id": lead_id, "dispatched": len(companies), "companies": companies}


@router.get("/list", response_model=List[LeadResponse])
async def list_leads(
    city: str = None,
    service_type: str = None,
    level: str = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """获取线索列表"""
    query = db.query(Lead)
    if city:
        query = query.filter(Lead.city == city)
    if service_type:
        query = query.filter(Lead.service_type == service_type)
    if level:
        query = query.filter(Lead.ai_level == level)

    leads = query.order_by(Lead.id.desc()).offset(offset).limit(limit).all()
    return leads
