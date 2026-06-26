# 技术合伙人交接文档

> **项目名称**：家政AI获客中台 (HouseKeep-AI)
> **负责人**：毛茸茸 (Chloe)
> **技术栈**：Python FastAPI + Vue3 + 微信小程序 + PostgreSQL + Redis

---

## 一、项目概述

### 1.1 一句话定位
用AI技术帮助家政公司低成本获取雇主客户。不做重资产，只做"AI市场部"。

### 1.2 核心架构
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  雇主小程序      │◄────►│  FastAPI后端      │◄────►│  Vue3 SaaS后台  │
│  (需求入口)      │      │  (AI引擎+API)     │      │  (公司管理端)   │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              PostgreSQL     Redis      OpenAI/Claude
              (业务数据)    (缓存)       (AI能力)
```

### 1.3 三大AI引擎
| 引擎 | 功能 | 技术实现 |
|------|------|----------|
| **AIGC内容引擎** | 自动生成小红书/抖音爆款内容 | Prompt模板 + GPT-4/Claude API |
| **线索评分引擎** | 评估雇主需求成交概率 | 14条规则 + NLP意图分析 + 完整度计算 |
| **智能分发引擎** | 把线索分配给最优家政公司 | 6因子加权匹配 + 动态定价 |

---

## 二、代码结构速览

```
housekeep-ai/
├── app/
│   ├── main.py              # FastAPI入口，自动创建数据表
│   ├── config.py            # pydantic-settings配置（读.env）
│   ├── database.py          # SQLAlchemy连接池
│   ├── models/              # 4个数据模型
│   │   ├── company.py       # 家政公司（信用分/VIP/余额）
│   │   ├── nanny.py         # 阿姨（技能/评分/视频）
│   │   ├── lead.py          # 线索 + 分发记录
│   │   └── content.py       # 内容模板 + 生成记录
│   ├── schemas/             # Pydantic数据校验（请求/响应）
│   ├── services/            # ⭐ 核心AI引擎（3个）
│   │   ├── ai_content.py    # AIGC：4种内容类型，支持GPT-4/Claude
│   │   ├── lead_scoring.py  # 评分：规则引擎+意图分析
│   │   └── lead_dispatch.py # 分发：区域/类型/预算/信用/响应/成交率
│   └── routers/             # API路由（4组REST API）
│       ├── leads.py         # 线索创建/评分/分发/列表
│       ├── companies.py     # 公司入驻/列表/充值
│       ├── contents.py      # AI内容生成
│       └── dashboard.py     # 数据看板（总览/城市/类型/排行）
├── frontend/saas/           # Vue3 + Element Plus + ECharts
│   ├── src/views/           # 6个页面
│   └── vite.config.js       # 代理到 localhost:8000
├── frontend/miniprogram/    # 微信小程序原生
│   ├── pages/               # 5个页面（首页/发布/找阿姨/详情/我的）
├── deploy/                  # 生产部署配置
│   ├── nginx.conf           # SSL反向代理
│   ├── docker-compose.prod.yml
│   └── deploy.sh            # 一键部署脚本
└── .github/workflows/ci.yml # GitHub Actions CI/CD
```

---

## 三、快速启动（5分钟跑起来）

### 3.1 后端
```bash
cd housekeep-ai

# 方式1：Docker（推荐）
docker-compose up -d          # 启动PostgreSQL + Redis
pip install -r requirements.txt
python scripts/init_db.py     # 建表
uvicorn app.main:app --reload  # 启动API

# 方式2：纯本地（需安装PostgreSQL+Redis）
# 复制 .env.example → .env，填入 OPENAI_API_KEY
cp .env.example .env
# 编辑 .env
uvicorn app.main:app --reload
```

### 3.2 Vue3 SaaS后台
```bash
cd frontend/saas
npm install
npm run dev     # http://localhost:5173
```

### 3.3 微信小程序
```bash
# 用微信开发者工具打开 frontend/miniprogram 目录
```

---

## 四、核心API速查

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/v1/housekeeping/leads/create` | POST | 雇主发布需求 → 自动AI评分 → 自动分发 |
| `/api/v1/housekeeping/leads/list` | GET | 线索列表（支持城市/类型/等级筛选） |
| `/api/v1/housekeeping/leads/{id}/score` | POST | 重新评分 |
| `/api/v1/housekeeping/leads/{id}/dispatch` | POST | 手动触发分发 |
| `/api/v1/housekeeping/contents/generate` | POST | AI生成营销内容 |
| `/api/v1/housekeeping/companies/create` | POST | 家政公司入驻 |
| `/api/v1/housekeeping/dashboard/overview` | GET | 数据看板总览 |

**完整API文档**：启动后端后访问 `http://localhost:8000/docs`

---

## 五、关键配置

### 5.1 环境变量（.env）
```
# 必填
DATABASE_URL=postgresql://housekeep:housekeep123@localhost:5432/housekeep_ai
OPENAI_API_KEY=sk-xxx          # 或 CLAUDE_API_KEY
SECRET_KEY=your-secret-key     # JWT密钥

# 选填
REDIS_URL=redis://localhost:6379/0
CLAUDE_API_KEY=sk-ant-xxx
```

### 5.2 GitHub Actions Secrets（仓库设置）
在 GitHub 仓库 Settings → Secrets → Actions 中添加：
- `DOCKER_USERNAME` / `DOCKER_PASSWORD`：Docker Hub账号
- `SSH_PRIVATE_KEY`：服务器SSH私钥
- `SERVER_HOST` / `SERVER_USER`：部署服务器信息

---

## 六、开发路线图

| 阶段 | 时间 | 任务 | 优先级 |
|------|------|------|--------|
| **MVP** | 0-2周 | 跑通后端API + 基础SaaS页面 | P0 |
| **内容引擎** | 2-4周 | AIGC接入真实AI API，积累Prompt模板 | P0 |
| **评分模型** | 4-6周 | 规则引擎 → XGBoost机器学习模型 | P1 |
| **分发优化** | 6-8周 | 强化学习分发，A/B测试 | P1 |
| **小程序上线** | 8-10周 | 微信小程序提交审核 | P1 |
| **教培扩展** | 3-6月 | 复制到家政+教培双行业 | P2 |

---

## 七、常见问题

**Q：AI内容生成调用真实API吗？**
> 当前代码支持OpenAI GPT-4和Claude，配置API Key后自动调用。没有Key时返回模拟数据。

**Q：数据库表怎么更新？**
> 修改 `app/models/` 下的模型后：
> ```bash
> alembic revision --autogenerate -m "描述"
> alembic upgrade head
> ```

**Q：怎么添加新的评分规则？**
> 编辑 `app/services/lead_scoring.py` 中的 `RULES` 列表，支持动态加减分和否决项。

**Q：前端怎么对接真实API？**
> Vue3的 `vite.config.js` 已配置代理到 `localhost:8000`。生产环境修改 `frontend/saas/src/api/index.js` 中的 `baseURL`。

---

## 八、联系方式

- **GitHub仓库**：https://github.com/chloeRong4822/housekeep-ai
- **本地API文档**：http://localhost:8000/docs
- **本地SaaS后台**：http://localhost:5173

---

*本文档由AI生成，如有疑问随时更新。*
