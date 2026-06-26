"""阿姨模型"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Nanny(Base):
    __tablename__ = "nannies"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    name = Column(String(64), comment="姓名")
    age = Column(Integer, comment="年龄")
    origin = Column(String(64), comment="籍贯")
    phone = Column(String(32))

    # 服务信息
    service_types = Column(JSON, default=list, comment="服务类型")
    work_years = Column(Integer, default=0, comment="工作年限")
    salary_expect = Column(Integer, comment="期望薪资")

    # 技能与认证
    skills = Column(JSON, default=list, comment="技能标签")
    certificates = Column(JSON, default=list, comment="证书列表")

    # 状态
    status = Column(Integer, default=0, comment="0待岗 1上户 2休假")

    # AI评分
    skill_score = Column(Float, default=0.0, comment="技能评分")
    stability_score = Column(Float, default=0.0, comment="稳定性评分")
    service_score = Column(Float, default=0.0, comment="服务评分")

    # 视频简历URL
    video_url = Column(String(512), comment="自我介绍视频")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
