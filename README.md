# 家政AI获客中台 (HouseKeep-AI)

家政行业的AI智能获客引擎。帮助家政公司低成本、规模化、精准化地获取雇主客户。

## 核心功能

- **AIGC内容引擎**：自动生成小红书/抖音爆款内容
- **线索质量评分**：AI评估雇主需求的成交概率
- **智能分发引擎**：将线索精准分配给最可能成交的家政公司
- **家政公司SaaS后台**：完整的获客管理工具
- **雇主小程序**：需求发布、阿姨浏览入口

## 技术栈

- **后端**：Python + FastAPI
- **数据库**：PostgreSQL + Redis
- **AI模型**：OpenAI GPT-4 / Claude API
- **搜索**：Elasticsearch
- **部署**：Docker + Docker Compose

## 快速开始

### 1. 环境准备

```bash
# 复制环境变量模板
cp .env.example .env
# 编辑 .env 填入你的配置
```

### 2. 本地开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Docker部署

```bash
docker-compose up -d
```

## API文档

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
housekeep-ai/
├── app/
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # SQLAlchemy数据模型
│   ├── routers/             # API路由
│   ├── services/            # 业务逻辑层
│   ├── schemas/             # Pydantic数据校验
│   └── utils/               # 工具函数
├── frontend/                # 前端代码
├── scripts/                 # 脚本工具
├── docker-compose.yml       # Docker编排
├── Dockerfile               # 容器镜像
└── requirements.txt         # Python依赖
```

## 核心模块说明

### AIGC内容引擎 (services/ai_content.py)
基于大模型API自动生成家政行业营销内容，支持小红书、抖音、朋友圈等平台。

### 线索评分引擎 (services/lead_scoring.py)
多维度评估雇主需求质量：需求完整度、文本意图、行为数据、历史成交率。

### 智能分发引擎 (services/lead_dispatch.py)
根据区域、服务类型、预算、响应速度、历史成交率等因子，将线索分配给最优家政公司。

### 需求预测模型 (services/prediction.py)
预测各区域各类阿姨的供需趋势，指导家政公司提前布局。

## 路线图

- [x] MVP核心功能
- [ ] 微信小程序雇主端
- [ ] SaaS后台管理端
- [ ] 强化学习优化分发
- [ ] 多行业扩展（教培/装修）

## License

MIT
