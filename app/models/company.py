"""家政公司模型"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, comment="公司名称")
    contact_name = Column(String(64), comment="联系人")
    phone = Column(String(32), comment="联系电话")
    email = Column(String(128), comment="邮箱")

    # 服务范围
    service_areas = Column(JSON, default=list, comment="服务区域列表")
    service_types = Column(JSON, default=list, comment="服务类型：育儿嫂/月嫂/保洁等")

    # 信用与评分
    credit_score = Column(Float, default=100.0, comment="信用分0-100")
    avg_response_time = Column(Float, default=0.0, comment="平均响应时间（分钟）")
    response_rate = Column(Float, default=0.0, comment="24小时响应率")
    completion_rate = Column(Float, default=0.0, comment="成交率")
    total_orders = Column(Integer, default=0, comment="累计成交单数")

    # VIP等级
    vip_level = Column(Integer, default=0, comment="0免费 1基础 2高级")
    vip_expire_at = Column(DateTime, comment="VIP到期时间")

    # 账户
    balance = Column(Float, default=0.0, comment="账户余额")
    status = Column(Integer, default=1, comment="0禁用 1启用")

    # 登录
    password_hash = Column(String(256))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
