"""智能分发引擎 - 将线索分配给最可能成交的家政公司"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.company import Company
from app.models.lead import Lead, LeadDispatch


class LeadDispatchService:
    """线索分发服务"""

    # 匹配因子权重
    FACTORS = {
        "location": {"weight": 0.25, "mandatory": True},
        "service_type": {"weight": 0.20, "mandatory": True},
        "budget": {"weight": 0.15, "mandatory": False},
        "credit": {"weight": 0.15, "mandatory": False},
        "response": {"weight": 0.10, "mandatory": False},
        "completion": {"weight": 0.10, "mandatory": False},
        "vip": {"weight": 0.05, "mandatory": False},
    }

    async def dispatch(
        self,
        db: Session,
        lead: Lead,
        max_companies: int = 3,
    ) -> List[Dict]:
        """
        分发线索
        返回: [{company_id, match_score, match_reason, charge}]
        """
        # 1. 硬条件过滤
        candidates = self._filter_candidates(db, lead)
        if not candidates:
            return []

        # 2. 多因子评分
        scored = []
        for company in candidates:
            score, reason = self._score_match(lead, company)
            scored.append((company, score, reason))

        # 3. 排序取TopN
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:max_companies]

        # 4. 扣费计算
        results = []
        for company, score, reason in top:
            charge = self._calc_charge(lead, company)
            results.append({
                "company_id": company.id,
                "company_name": company.name,
                "match_score": round(score, 1),
                "match_reason": reason,
                "charge": charge,
            })

        return results

    def _filter_candidates(self, db: Session, lead: Lead) -> List[Company]:
        """硬条件过滤候选公司"""
        query = db.query(Company).filter(Company.status == 1)

        # 区域匹配
        if lead.district:
            # 简化：检查service_areas是否包含该区域
            companies = query.all()
            matched = []
            for c in companies:
                areas = c.service_areas or []
                if lead.district in areas or lead.city in areas:
                    matched.append(c)
            return matched

        return query.all()

    def _score_match(self, lead: Lead, company: Company) -> tuple:
        """计算匹配分数"""
        score = 0.0
        reasons = []

        # 区域匹配
        if lead.district and company.service_areas:
            if lead.district in company.service_areas:
                score += 25
                reasons.append("服务区域完全匹配")
            elif lead.city in company.service_areas:
                score += 15
                reasons.append("服务城市匹配")

        # 服务类型匹配
        if lead.service_type and company.service_types:
            if lead.service_type in company.service_types:
                score += 20
                reasons.append(f"提供{lead.service_type}服务")

        # 预算匹配
        if lead.budget_max and lead.budget_max >= 5000:
            score += 10
            reasons.append("预算充足")

        # 信用分
        if company.credit_score >= 80:
            score += 15
            reasons.append("信用优秀")
        elif company.credit_score >= 60:
            score += 8
            reasons.append("信用良好")

        # 响应速度
        if company.response_rate >= 0.9:
            score += 10
            reasons.append("响应迅速")

        # 成交率
        if company.completion_rate >= 0.3:
            score += 10
            reasons.append("成交率高")

        # VIP等级
        if company.vip_level >= 2:
            score += 5
            reasons.append("高级会员")

        reason_text = "；".join(reasons[:4]) if reasons else "基础匹配"
        return score, reason_text

    def _calc_charge(self, lead: Lead, company: Company) -> float:
        """计算线索费用"""
        base_price = 80.0

        # 根据评分调价
        if lead.ai_score >= 80:
            base_price *= 1.5
        elif lead.ai_score >= 60:
            base_price *= 1.2

        # VIP折扣
        if company.vip_level >= 2:
            base_price *= 0.8

        return round(base_price, 2)
