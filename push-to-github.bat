@echo off
chcp 65001 > nul
echo ==========================================
echo   家政AI获客中台 - GitHub推送助手
echo ==========================================
echo.

REM 检查Git
where git > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [错误] Git未安装，请先安装Git
    pause
    exit /b 1
)

echo [1/3] Git已就绪
echo.

REM 询问GitHub用户名
set /p GITHUB_USER=请输入你的GitHub用户名:
if "%GITHUB_USER%"=="" (
    echo 用户名不能为空
    pause
    exit /b 1
)

echo.
echo [2/3] 配置远程仓库...
cd /d "C:\Users\dullon\Desktop\housekeep-ai"
git remote remove origin 2> nul
git remote add origin https://github.com/%GITHUB_USER%/housekeep-ai.git
git branch -M main

echo.
echo [3/3] 推送到GitHub...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ==========================================
    echo   ✅ 推送成功！
    echo   仓库地址: https://github.com/%GITHUB_USER%/housekeep-ai
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo   ❌ 推送失败
    echo   请检查：
    echo   1. GitHub用户名是否正确
    echo   2. 仓库是否已在GitHub创建
    echo   3. 是否已登录GitHub
    echo ==========================================
    echo.
    echo 如果提示输入密码，请使用Personal Access Token代替密码。
    echo 生成Token: https://github.com/settings/tokens/new
)

pause
