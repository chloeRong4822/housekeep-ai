"""FastAPI应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import leads, companies, contents, dashboard

# 创建数据表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="家政AI获客中台",
    description="AI驱动的家政行业智能获客引擎",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(leads.router)
app.include_router(companies.router)
app.include_router(contents.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "name": "家政AI获客中台",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
