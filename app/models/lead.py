"""线索模型"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    # 雇主信息
    employer_name = Column(String(64), comment="雇主姓名")
    employer_phone = Column(String(32), comment="雇主电话")
    employer_wechat = Column(String(64), comment="微信号")

    # 需求信息
    service_type = Column(String(32), comment="服务类型")
    service_form = Column(String(32), comment="住家/白班/钟点")
    city = Column(String(32), comment="城市")
    district = Column(String(64), comment="区域")
    address = Column(String(256), comment="详细地址")

    # 家庭信息
    family_size = Column(Integer, comment="家庭人数")
    has_pet = Column(Integer, default=0, comment="0无 1有")
    baby_age = Column(Integer, comment="宝宝月龄")
    elderly_count = Column(Integer, default=0, comment="老人数量")

    # 预算与时间
    budget_min = Column(Integer, comment="预算下限")
    budget_max = Column(Integer, comment="预算上限")
    expect_date = Column(DateTime, comment="期望上岗时间")
    urgency = Column(Integer, default=0, comment="0不急 1一般 2急")

    # 偏好
    preference = Column(JSON, default=dict, comment="偏好：性格/经验/年龄等")

    # AI评分
    ai_score = Column(Float, default=0.0, comment="AI评分0-100")
    ai_level = Column(String(16), default="medium", comment="high/medium/low/invalid")
    ai_reason = Column(Text, comment="评分理由")

    # 来源
    source = Column(String(32), default="miniprogram", comment="miniprogram/xiaohongshu/douyin")
    status = Column(Integer, default=0, comment="0待分发 1已分发 2已成交 3已失效")

    # 行为数据
    view_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    consult_count = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class LeadDispatch(Base):
    __tablename__ = "lead_dispatches"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # 匹配信息
    match_score = Column(Float, default=0.0, comment="匹配度")
    match_reason = Column(Text, comment="匹配理由")

    # 状态
    status = Column(Integer, default=0, comment="0待响应 1已查看 2已联系 3已成交 4已放弃")

    # 费用
    charge = Column(Float, default=0.0, comment="线索费用")

    # 响应时间
    viewed_at = Column(DateTime)
    contacted_at = Column(DateTime)
    deal_at = Column(DateTime)

    created_at = Column(DateTime, server_default=func.now())
