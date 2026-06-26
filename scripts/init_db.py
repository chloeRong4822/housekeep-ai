"""初始化数据库"""
import sys
sys.path.insert(0, "C:\\Users\\dullon\\Desktop\\housekeep-ai")

from app.database import engine, Base
from app.models.company import Company
from app.models.nanny import Nanny
from app.models.lead import Lead, LeadDispatch
from app.models.content import ContentTemplate, GeneratedContent


def init():
    print("正在创建数据表...")
    Base.metadata.create_all(bind=engine)
    print("数据表创建完成！")

    # 可以在这里插入测试数据
    print("可以运行 uvicorn app.main:app --reload 启动服务")


if __name__ == "__main__":
    init()
