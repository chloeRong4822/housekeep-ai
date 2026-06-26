# 🏠 家政AI获客中台 (HouseKeep-AI)

> **AI驱动的家政行业智能获客引擎**
>
> 让每一家家政公司都能用AI低成本找到客户。

[![CI/CD](https://github.com/chloeRong4822/housekeep-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/chloeRong4822/housekeep-ai/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg)](https://fastapi.tiangolo.com/)
[![Vue 3](https://img.shields.io/badge/Vue-3.4-4FC08D.svg)](https://vuejs.org/)

---

## ✨ 核心功能

| 模块 | 功能 | 技术亮点 |
|------|------|----------|
| 🤖 **AIGC内容引擎** | 一键生成小红书/抖音爆款内容 | GPT-4/Claude + Prompt模板库 |
| 📊 **线索质量评分** | AI评估雇主需求成交概率 | 14条规则 + NLP意图分析 |
| 🎯 **智能分发引擎** | 把线索精准分配给最优家政公司 | 6因子加权匹配 + 动态定价 |
| 📈 **数据预测模型** | 预测各区域供需趋势 | 时间序列 + 机器学习 |

---

## 🏗️ 系统架构

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  雇主小程序   │◄────►│  FastAPI     │◄────►│  Vue3 SaaS   │
│  (需求入口)   │      │  AI引擎      │      │  公司管理端   │
└──────────────┘      └──────────────┘      └──────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
      PostgreSQL        Redis           OpenAI/Claude
      (业务数据)       (缓存)            (AI能力)
```

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/chloeRong4822/housekeep-ai.git
cd housekeep-ai
```

### 2. 启动后端（Docker）

```bash
docker-compose up -d          # 启动PostgreSQL + Redis
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填入 OPENAI_API_KEY
python scripts/init_db.py     # 初始化数据库
uvicorn app.main:app --reload  # 启动API
```

API文档：`http://localhost:8000/docs`

### 3. 启动SaaS后台

```bash
cd frontend/saas
npm install
npm run dev
```

访问：`http://localhost:5173`

### 4. 打开微信小程序

用微信开发者工具打开 `frontend/miniprogram` 目录。

---

## 📡 核心API

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/v1/housekeeping/leads/create` | POST | 雇主发布需求 → AI评分 → 自动分发 |
| `/api/v1/housekeeping/contents/generate` | POST | AI生成营销内容 |
| `/api/v1/housekeeping/dashboard/overview` | GET | 数据看板总览 |

[查看完整API示例 →](API_EXAMPLES.md)

---

## 📁 项目结构

```
housekeep-ai/
├── app/                    # FastAPI后端
│   ├── models/             # SQLAlchemy数据模型
│   ├── services/           # ⭐ 核心AI引擎（3个）
│   ├── routers/            # API路由
│   └── schemas/            # Pydantic数据校验
├── frontend/
│   ├── saas/               # Vue3家政公司后台
│   └── miniprogram/        # 雇主微信小程序
├── deploy/                 # 生产部署配置
└── .github/workflows/      # CI/CD自动部署
```

[查看技术交接文档 →](TECH-HANDOVER.md)

---

## 🛠️ 技术栈

- **后端**：Python 3.11 + FastAPI + SQLAlchemy + Alembic
- **数据库**：PostgreSQL 15 + Redis 7
- **AI**：OpenAI GPT-4 / Claude API
- **前端**：Vue 3 + Vite + Element Plus + ECharts
- **小程序**：微信小程序原生
- **部署**：Docker + Docker Compose + Nginx
- **CI/CD**：GitHub Actions

---

## 🗺️ 路线图

- [x] MVP核心功能（后端API + SaaS后台 + 小程序）
- [x] AIGC内容引擎
- [x] 线索评分与分发
- [x] Docker部署配置
- [x] GitHub Actions CI/CD
- [ ] 微信小程序上线
- [ ] 强化学习优化分发
- [ ] 多行业扩展（教培/装修）

---

## 📄 文档

- [技术交接文档](TECH-HANDOVER.md) - 给技术合伙人的详细指南
- [部署指南](DEPLOY.md) - 生产环境部署（Docker/裸机/自动部署）
- [API示例](API_EXAMPLES.md) - 接口调用示例

---

## 🤝 贡献

欢迎提交Issue和PR！

---

## 📜 License

MIT

---

*用AI重构万亿家政市场 🚀*
