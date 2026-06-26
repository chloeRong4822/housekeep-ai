# 生产环境部署指南

## 方案一：Docker Compose 一键部署（推荐）

### 前置条件
- 一台Linux服务器（CentOS/Ubuntu/Debian）
- Docker + Docker Compose 已安装
- 域名已解析到服务器
- SSL证书（可用Let's Encrypt免费申请）

### 1. 服务器准备

```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 创建项目目录
mkdir -p /opt/housekeep-ai
cd /opt/housekeep-ai
```

### 2. 拉取代码并配置

```bash
git clone https://github.com/chloeRong4822/housekeep-ai.git .

# 复制生产环境配置
cp .env.example .env.production

# 编辑配置
nano .env.production
```

`.env.production` 内容：
```
DATABASE_URL=postgresql://housekeep:your-strong-password@db:5432/housekeep_ai
REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=sk-your-openai-key
SECRET_KEY=your-very-long-random-secret-key
DEBUG=false
```

### 3. 启动服务

```bash
cd deploy

# 修改 docker-compose.prod.yml 中的环境变量
nano docker-compose.prod.yml

# 启动所有服务
docker-compose -f docker-compose.prod.yml up -d

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f api
```

### 4. 初始化数据库

```bash
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head
```

### 5. 配置Nginx + SSL

```bash
# 复制nginx配置
sudo cp deploy/nginx.conf /etc/nginx/conf.d/housekeep-ai.conf

# 申请Let's Encrypt证书
sudo certbot --nginx -d your-domain.com

# 重启nginx
sudo systemctl reload nginx
```

### 6. 验证部署

```bash
# 检查API
curl https://your-domain.com/api/v1/housekeeping/health

# 应该返回 {"status":"ok"}
```

---

## 方案二：裸机部署（不使用Docker）

### 1. 安装依赖

```bash
# Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# PostgreSQL 15
sudo apt install postgresql-15 postgresql-contrib

# Redis 7
sudo apt install redis-server

# Nginx
sudo apt install nginx
```

### 2. 配置PostgreSQL

```bash
sudo -u postgres psql -c "CREATE USER housekeep WITH PASSWORD 'your-password';"
sudo -u postgres psql -c "CREATE DATABASE housekeep_ai OWNER housekeep;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE housekeep_ai TO housekeep;"
```

### 3. 部署后端

```bash
cd /opt/housekeep-ai
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
export DATABASE_URL="postgresql://housekeep:your-password@localhost:5432/housekeep_ai"
export REDIS_URL="redis://localhost:6379/0"
export OPENAI_API_KEY="sk-xxx"
export SECRET_KEY="your-secret"
export DEBUG="false"

# 初始化数据库
alembic upgrade head

# 启动（生产环境用systemd或supervisor）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. 配置Systemd服务

创建 `/etc/systemd/system/housekeep-ai.service`：

```ini
[Unit]
Description=HouseKeep AI API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/housekeep-ai
Environment=PATH=/opt/housekeep-ai/venv/bin
EnvironmentFile=/opt/housekeep-ai/.env.production
ExecStart=/opt/housekeep-ai/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable housekeep-ai
sudo systemctl start housekeep-ai
sudo systemctl status housekeep-ai
```

---

## 方案三：GitHub Actions 自动部署

### 1. 配置服务器SSH

在服务器上生成部署密钥：
```bash
ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions
# 复制公钥到authorized_keys
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
```

### 2. 配置GitHub Secrets

在仓库 Settings → Secrets → Actions 中添加：
- `SSH_PRIVATE_KEY`：服务器私钥内容
- `SERVER_HOST`：服务器IP或域名
- `SERVER_USER`：服务器用户名（如ubuntu）
- `DOCKER_USERNAME` / `DOCKER_PASSWORD`：Docker Hub账号

### 3. 自动部署流程

每次推送到 `main` 分支时，GitHub Actions会自动：
1. 运行测试
2. 构建Docker镜像
3. 推送到Docker Hub
4. SSH到服务器拉取并重启

---

## 常用运维命令

```bash
# 查看日志
docker-compose -f deploy/docker-compose.prod.yml logs -f api
docker-compose -f deploy/docker-compose.prod.yml logs -f db

# 重启服务
docker-compose -f deploy/docker-compose.prod.yml restart api

# 备份数据库
docker-compose -f deploy/docker-compose.prod.yml exec db pg_dump -U housekeep housekeep_ai > backup.sql

# 进入容器
docker-compose -f deploy/docker-compose.prod.yml exec api bash

# 数据库迁移
docker-compose -f deploy/docker-compose.prod.yml exec api alembic upgrade head
```

---

## 性能优化建议

1. **启用Redis缓存**：配置Redis缓存热点数据（公司画像、评分规则）
2. **数据库索引**：为高频查询字段添加索引（lead.city, lead.service_type, company.service_areas）
3. **CDN加速**：静态资源使用CDN（微信小程序图片、SaaS前端资源）
4. **数据库连接池**：调整SQLAlchemy连接池大小
5. **异步处理**：耗时操作（AI内容生成）改为Celery异步队列
