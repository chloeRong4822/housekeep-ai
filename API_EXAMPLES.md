# API调用示例

## 基础信息
- Base URL: `http://localhost:8000`
- API文档: `http://localhost:8000/docs`

---

## 1. 创建线索（雇主发布需求）

```bash
curl -X POST "http://localhost:8000/api/v1/housekeeping/leads/create" \
  -H "Content-Type: application/json" \
  -d '{
    "employer_name": "张女士",
    "employer_phone": "13800138000",
    "service_type": "育儿嫂",
    "city": "成都",
    "district": "高新区",
    "budget_min": 7000,
    "budget_max": 9000,
    "family_size": 3,
    "baby_age": 6,
    "urgency": 2,
    "preference": {
      "性格": "细心",
      "经验": "3年以上",
      "年龄": "40-50岁"
    }
  }'
```

**返回：**
```json
{
  "id": 1,
  "employer_name": "张女士",
  "employer_phone": "13800138000",
  "service_type": "育儿嫂",
  "city": "成都",
  "ai_score": 87.5,
  "ai_level": "high",
  "ai_reason": "评分87.5分（高意向）。主要依据：+15:有预算；+20:预算充足...",
  "status": 1,
  "created_at": "2024-06-26T10:00:00"
}
```

---

## 2. AI生成内容（小红书）

```bash
curl -X POST "http://localhost:8000/api/v1/housekeeping/contents/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "xiaohongshu",
    "content_type": "nanny_show",
    "city": "成都",
    "service_type": "育儿嫂",
    "target_audience": "新手妈妈",
    "style": "friendly",
    "count": 3
  }'
```

**返回：**
```json
{
  "contents": [
    {
      "title": "成都宝妈注意！这个月嫂有8年经验，带过30多个宝宝",
      "body": "正文内容...",
      "image_desc": "阿姨微笑照+宝宝互动照",
      "hashtags": ["#成都月嫂", "#月嫂推荐", "#新手妈妈"],
      "suggested_time": "20:00"
    }
  ]
}
```

---

## 3. 创建家政公司

```bash
curl -X POST "http://localhost:8000/api/v1/housekeeping/companies/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "和阳家政",
    "contact_name": "王经理",
    "phone": "13900139000",
    "service_areas": ["高新区", "锦江区", "武侯区"],
    "service_types": ["育儿嫂", "月嫂", "保洁"]
  }'
```

---

## 4. 获取线索列表

```bash
curl "http://localhost:8000/api/v1/housekeeping/leads/list?city=成都&level=high"
```

---

## 5. 获取数据看板

```bash
curl "http://localhost:8000/api/v1/housekeeping/dashboard/overview"
```

**返回：**
```json
{
  "total_leads": 1000,
  "today_leads": 35,
  "week_leads": 210,
  "total_companies": 50,
  "total_deals": 120,
  "avg_ai_score": 72.5,
  "conversion_rate": 12.0
}
```

---

## 6. 手动分发线索

```bash
curl -X POST "http://localhost:8000/api/v1/housekeeping/leads/1/dispatch"
```

**返回：**
```json
{
  "lead_id": 1,
  "dispatched": 3,
  "companies": [
    {
      "company_id": 1,
      "company_name": "和阳家政",
      "match_score": 95.0,
      "match_reason": "服务区域完全匹配；提供育儿嫂服务；预算充足",
      "charge": 120.0
    }
  ]
}
```
