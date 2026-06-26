#!/bin/bash
set -e

echo "=== 家政AI获客中台 部署脚本 ==="

# 配置
PROJECT_DIR="/opt/housekeep-ai"
DOMAIN="your-domain.com"

echo "[1/6] 更新代码..."
cd $PROJECT_DIR
git pull origin main

echo "[2/6] 构建后端..."
docker-compose build api

echo "[3/6] 启动服务..."
docker-compose up -d

echo "[4/6] 执行数据库迁移..."
docker-compose exec -T api alembic upgrade head

echo "[5/6] 构建前端..."
cd $PROJECT_DIR/frontend/saas
npm install
npm run build

# 复制到nginx目录
cp -r dist/* /var/www/housekeep-saas/

echo "[6/6] 重启nginx..."
systemctl reload nginx

echo "=== 部署完成 ==="
echo "API: https://$DOMAIN/api/"
echo "SaaS: https://$DOMAIN/"
