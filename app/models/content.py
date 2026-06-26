"""内容模板与生成内容模型"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class ContentTemplate(Base):
    __tablename__ = "content_templates"

    id = Column(Integer, primary_key=True, index=True)

    # 模板信息
    template_name = Column(String(128), comment="模板名称")
    template_type = Column(String(32), comment="类型：hook/problem/solution/proof/cta")
    platform = Column(String(32), comment="平台：xiaohongshu/douyin/wechat")
    industry = Column(String(32), default="housekeeping", comment="行业")

    # Prompt模板
    prompt_template = Column(Text, comment="Prompt模板（含占位符）")
    example_json = Column(JSON, default=dict, comment="示例数据")

    # 效果数据
    avg_score = Column(Float, default=0.0, comment="平均效果评分")
    use_count = Column(Integer, default=0)
    click_rate = Column(Float, default=0.0, comment="点击率")
    lead_rate = Column(Float, default=0.0, comment="线索转化率")

    status = Column(Integer, default=1, comment="0禁用 1启用")
    created_at = Column(DateTime, server_default=func.now())


class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, comment="所属公司")
    template_id = Column(Integer, comment="使用的模板")

    # 内容
    platform = Column(String(32))
    title = Column(Text)
    body = Column(Text)
    image_desc = Column(Text, comment="配图描述")
    hashtags = Column(JSON, default=list, comment="话题标签")
    suggested_time = Column(String(16), comment="建议发布时间")

    # 效果
    is_published = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    collects = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    leads = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
