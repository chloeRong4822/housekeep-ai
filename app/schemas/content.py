"""内容生成Schema"""
from pydantic import BaseModel, Field
from typing import Optional, List


class ContentGenerateRequest(BaseModel):
    """生成内容请求"""
    platform: str = Field(..., description="平台：xiaohongshu/douyin/wechat")
    content_type: str = Field(..., description="类型：nanny_show/guide/case/promo")
    city: str
    service_type: str
    nanny_id: Optional[int] = None
    target_audience: Optional[str] = None
    selling_point: Optional[str] = None
    style: str = "friendly"
    count: int = 3


class ContentItem(BaseModel):
    title: str
    body: str
    image_desc: str
    hashtags: List[str]
    suggested_time: str


class ContentGenerateResponse(BaseModel):
    contents: List[ContentItem]
