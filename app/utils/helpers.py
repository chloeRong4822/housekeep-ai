"""工具函数"""
import re
from typing import Dict, Any


def clean_phone(phone: str) -> str:
    """清洗手机号"""
    return re.sub(r"[^0-9]", "", phone)


def mask_phone(phone: str) -> str:
    """脱敏手机号"""
    if len(phone) == 11:
        return phone[:3] + "****" + phone[7:]
    return phone


def safe_json_loads(text: str, default: Any = None) -> Any:
    """安全解析JSON"""
    import json
    try:
        return json.loads(text)
    except:
        return default
