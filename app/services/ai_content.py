"""AIGC内容引擎 - 自动生成家政行业营销内容"""
import httpx
import json
from typing import List, Dict, Optional
from app.config import get_settings


class AIContentService:
    """AI内容生成服务"""

    # 行业Prompt模板库
    PROMPT_TEMPLATES = {
        "nanny_show": {
            "system": "你是一位家政行业资深内容运营，擅长在小红书/抖音上创作高转化内容。",
            "user": """请为{platform}生成一篇阿姨展示类内容。

城市：{city}
服务类型：{service_type}
目标人群：{target_audience}
核心卖点：{selling_point}
风格：{style}

要求：
1. 标题吸引人，使用emoji，3秒内抓住注意力
2. 正文包含一个真实感案例，有具体数字和细节
3. 突出阿姨的专业性和温度
4. 结尾引导互动（评论/私信）
5. 字数：小红书300-500字，抖音脚本30-45秒
6. 提供3-5个话题标签

请按以下JSON格式输出：
{{
    "title": "标题",
    "body": "正文",
    "image_desc": "配图描述",
    "hashtags": ["标签1", "标签2"],
    "suggested_time": "建议发布时间"
}}"""
        },
        "guide": {
            "system": "你是一位家政行业避坑专家，擅长写干货内容。",
            "user": """请为{platform}生成一篇避坑指南类内容。

城市：{city}
主题：{service_type}避坑
目标人群：{target_audience}

要求：
1. 标题使用数字法或悬念法
2. 列出3-5个具体避坑点，每个点有解释和建议
3. 语言亲切，像朋友提醒
4. 结尾引导收藏和转发
5. 字数：小红书500-800字

请按JSON格式输出：
{{
    "title": "标题",
    "body": "正文",
    "image_desc": "配图描述",
    "hashtags": ["标签1", "标签2"],
    "suggested_time": "建议发布时间"
}}"""
        },
        "case": {
            "system": "你是一位擅长讲故事的家政行业内容创作者。",
            "user": """请为{platform}生成一篇真实雇主故事。

城市：{city}
服务类型：{service_type}
核心卖点：{selling_point}

要求：
1. 以雇主第一人称视角讲述
2. 有冲突（遇到问题）- 转折（找到阿姨）- 结果（满意）的结构
3. 包含具体数字和细节
4. 真实感强，不夸张
5. 结尾自然引导咨询

请按JSON格式输出。"""
        },
        "promo": {
            "system": "你是一位家政行业促销活动策划。",
            "user": """请为{platform}生成一篇促销活动内容。

城市：{city}
服务类型：{service_type}
优惠内容：{selling_point}

要求：
1. 制造紧迫感（限时/限量）
2. 清晰说明优惠内容
3. 降低决策门槛
4. 结尾强烈CTA

请按JSON格式输出。"""
        }
    }

    def __init__(self):
        self.settings = get_settings()
        self.client = httpx.AsyncClient(timeout=60.0)

    async def generate_content(
        self,
        platform: str,
        content_type: str,
        city: str,
        service_type: str,
        target_audience: str = "新手妈妈",
        selling_point: str = "",
        style: str = "friendly",
        count: int = 3,
    ) -> List[Dict]:
        """生成内容"""
        template = self.PROMPT_TEMPLATES.get(content_type, self.PROMPT_TEMPLATES["nanny_show"])

        contents = []
        for i in range(count):
            user_prompt = template["user"].format(
                platform=platform,
                city=city,
                service_type=service_type,
                target_audience=target_audience,
                selling_point=selling_point or f"专业{service_type}服务",
                style=style,
            )

            try:
                content = await self._call_llm(template["system"], user_prompt)
                contents.append(content)
            except Exception as e:
                contents.append({
                    "title": f"{city}专业{service_type}推荐",
                    "body": f"{service_type}服务，经验丰富，值得信赖。",
                    "image_desc": "阿姨微笑照",
                    "hashtags": [f"#{city}{service_type}", "#家政推荐"],
                    "suggested_time": "20:00",
                    "error": str(e),
                })

        return contents

    async def _call_llm(self, system: str, user: str) -> Dict:
        """调用大模型API"""
        settings = self.settings

        if settings.openai_api_key:
            return await self._call_openai(system, user)
        elif settings.claude_api_key:
            return await self._call_claude(system, user)
        else:
            raise ValueError("未配置AI API密钥")

    async def _call_openai(self, system: str, user: str) -> Dict:
        """调用OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.settings.openai_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.8,
        }

        resp = await self.client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
        )
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"]

        # 解析JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._parse_json_from_text(content)

    async def _call_claude(self, system: str, user: str) -> Dict:
        """调用Claude API"""
        headers = {
            "x-api-key": self.settings.claude_api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        data = {
            "model": self.settings.claude_model,
            "max_tokens": 2000,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }

        resp = await self.client.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
        )
        resp.raise_for_status()
        result = resp.json()
        content = result["content"][0]["text"]

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._parse_json_from_text(content)

    @staticmethod
    def _parse_json_from_text(text: str) -> Dict:
        """从文本中提取JSON"""
        import re
        pattern = r"\{[\s\S]*\}"
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
        return {
            "title": "AI生成内容",
            "body": text[:500],
            "image_desc": "配图",
            "hashtags": ["#家政"],
            "suggested_time": "20:00",
        }
