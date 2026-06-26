"""线索质量评分引擎 - 评估雇主需求的成交概率"""
import re
from typing import Dict, Tuple
from app.schemas.lead import LeadCreate


class LeadScoringService:
    """线索评分服务"""

    # 评分规则配置
    RULES = [
        # 否决项
        {"name": "电话为空", "check": lambda d: not d.get("employer_phone"), "score": -100, "is_veto": True},
        {"name": "服务类型为空", "check": lambda d: not d.get("service_type"), "score": -100, "is_veto": True},
        {"name": "城市为空", "check": lambda d: not d.get("city"), "score": -100, "is_veto": True},

        # 硬条件加分
        {"name": "有预算", "check": lambda d: d.get("budget_min") or d.get("budget_max"), "score": 15},
        {"name": "预算充足", "check": lambda d: (d.get("budget_max") or 0) >= 8000, "score": 20},
        {"name": "有详细地址", "check": lambda d: d.get("address"), "score": 10},
        {"name": "有区域", "check": lambda d: d.get("district"), "score": 10},
        {"name": "有期望时间", "check": lambda d: d.get("expect_date"), "score": 15},
        {"name": "紧急需求", "check": lambda d: d.get("urgency") >= 2, "score": 20},
        {"name": "有微信号", "check": lambda d: d.get("employer_wechat"), "score": 10},
        {"name": "有姓名", "check": lambda d: d.get("employer_name"), "score": 5},
        {"name": "有家庭信息", "check": lambda d: d.get("family_size") or d.get("baby_age"), "score": 10},
        {"name": "有偏好", "check": lambda d: d.get("preference") and len(d.get("preference", {})) > 0, "score": 10},

        # 减分项
        {"name": "预算过低", "check": lambda d: (d.get("budget_max") or 99999) < 4000, "score": -20},
        {"name": "不急", "check": lambda d: d.get("urgency") == 0, "score": -10},
    ]

    # 文本意图分析关键词
    INTENT_KEYWORDS = {
        "high": ["急", "马上", "立刻", "越快越好", "这周", "明天", "必须", "急需"],
        "low": ["先了解", "看看", "问问", "参考", "了解一下", "大概", "以后"],
    }

    async def score(self, lead_data: LeadCreate) -> Tuple[float, str, str, Dict]:
        """
        评分入口
        返回: (分数, 等级, 理由, 特征)
        """
        data = lead_data.model_dump()
        score = 50.0  # 基础分
        reasons = []
        features = {}

        # 执行规则评分
        for rule in self.RULES:
            if rule["check"](data):
                score += rule["score"]
                if rule.get("is_veto"):
                    reasons.append(f"否决: {rule['name']}")
                    return 0.0, "invalid", f"{rule['name']}，线索无效", {"veto": rule["name"]}
                elif rule["score"] > 0:
                    reasons.append(f"+{rule['score']}: {rule['name']}")
                else:
                    reasons.append(f"{rule['score']}: {rule['name']}")

        # 文本意图分析
        all_text = f"{data.get('service_type', '')} {str(data.get('preference', ''))}"
        intent_score = self._analyze_intent(all_text)
        score += intent_score
        features["intent_score"] = intent_score
        if intent_score > 0:
            reasons.append(f"+{intent_score}: 意图强烈")
        elif intent_score < 0:
            reasons.append(f"{intent_score}: 意图较弱")

        # 完整性评分
        completeness = self._calc_completeness(data)
        score += completeness * 0.3
        features["completeness"] = round(completeness, 1)
        reasons.append(f"+{round(completeness * 0.3, 1)}: 信息完整度{completeness}分")

        # 最终分数限制
        score = max(0, min(100, score))
        features["final_score"] = round(score, 1)

        # 确定等级
        if score >= 80:
            level = "high"
            level_desc = "高意向"
        elif score >= 50:
            level = "medium"
            level_desc = "中意向"
        else:
            level = "low"
            level_desc = "低意向"

        reason_text = f"评分{round(score)}分（{level_desc}）。"
        reason_text += "主要依据：" + "；".join(reasons[:5])

        return round(score, 1), level, reason_text, features

    def _analyze_intent(self, text: str) -> float:
        """分析文本意图强度"""
        if not text:
            return 0.0

        score = 0.0
        for keyword in self.INTENT_KEYWORDS["high"]:
            if keyword in text:
                score += 8.0
        for keyword in self.INTENT_KEYWORDS["low"]:
            if keyword in text:
                score -= 5.0

        return score

    def _calc_completeness(self, data: Dict) -> float:
        """计算信息完整度"""
        required_fields = [
            "employer_phone", "service_type", "city", "district",
            "budget_min", "budget_max", "expect_date", "preference"
        ]
        filled = sum(1 for f in required_fields if data.get(f))
        return (filled / len(required_fields)) * 100
