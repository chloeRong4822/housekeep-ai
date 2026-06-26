"""内容生成路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.content import ContentGenerateRequest, ContentGenerateResponse, ContentItem
from app.services.ai_content import AIContentService
from app.models.content import GeneratedContent

router = APIRouter(prefix="/api/v1/housekeeping/contents", tags=["AI内容"])


@router.post("/generate", response_model=ContentGenerateResponse)
async def generate_content(data: ContentGenerateRequest, db: Session = Depends(get_db)):
    """AI生成营销内容"""
    service = AIContentService()
    raw_contents = await service.generate_content(
        platform=data.platform,
        content_type=data.content_type,
        city=data.city,
        service_type=data.service_type,
        target_audience=data.target_audience,
        selling_point=data.selling_point,
        style=data.style,
        count=data.count,
    )

    contents = []
    for raw in raw_contents:
        item = ContentItem(
            title=raw.get("title", ""),
            body=raw.get("body", ""),
            image_desc=raw.get("image_desc", ""),
            hashtags=raw.get("hashtags", []),
            suggested_time=raw.get("suggested_time", "20:00"),
        )
        contents.append(item)

        # 保存到数据库
        gc = GeneratedContent(
            platform=data.platform,
            title=item.title,
            body=item.body,
            image_desc=item.image_desc,
            hashtags=item.hashtags,
            suggested_time=item.suggested_time,
        )
        db.add(gc)

    db.commit()
    return ContentGenerateResponse(contents=contents)
