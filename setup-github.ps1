# 家政AI获客中台 - GitHub一键推送脚本
Write-Host "=== 家政AI获客中台 GitHub推送助手 ===" -ForegroundColor Cyan

$repoName = "housekeep-ai"

# Step 1: 检查并安装 gh CLI
Write-Host "`n[1/5] 检查 GitHub CLI..." -ForegroundColor Yellow
$gh = Get-Command gh -ErrorAction SilentlyContinue
if (-not $gh) {
    Write-Host "正在安装 GitHub CLI..." -ForegroundColor Yellow
    winget install --id GitHub.cli -e --accept-source-agreements --accept-package-agreements
    # 刷新环境变量
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    $gh = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $gh) {
        Write-Host "安装失败，请手动下载: https://cli.github.com/" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ GitHub CLI 已就绪" -ForegroundColor Green

# Step 2: 检查登录状态
Write-Host "`n[2/5] 检查 GitHub 登录状态..." -ForegroundColor Yellow
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "需要登录 GitHub，正在打开浏览器..." -ForegroundColor Yellow
    gh auth login --web
    Write-Host "请在浏览器中完成授权，然后按回车继续..." -ForegroundColor Cyan
    [void][System.Console]::ReadLine()
} else {
    Write-Host "✅ 已登录 GitHub" -ForegroundColor Green
}

# Step 3: 获取用户名
Write-Host "`n[3/5] 获取 GitHub 用户名..." -ForegroundColor Yellow
$username = gh api user -q .login
Write-Host "用户名: $username" -ForegroundColor Green

# Step 4: 创建仓库
Write-Host "`n[4/5] 创建 GitHub 仓库..." -ForegroundColor Yellow
$repoExists = gh repo view "$username/$repoName" 2>&1
if ($LASTEXITCODE -ne 0) {
    gh repo create $repoName --public --source=. --push
    Write-Host "✅ 仓库创建并推送完成!" -ForegroundColor Green
} else {
    Write-Host "仓库已存在，直接推送..." -ForegroundColor Yellow
    cd C:\Users\dullon\Desktop\housekeep-ai
    git remote add origin "https://github.com/$username/$repoName.git" 2>$null
    git branch -M main
    git push -u origin main
    Write-Host "✅ 推送完成!" -ForegroundColor Green
}

# Step 5: 输出结果
Write-Host "`n[5/5] 完成!" -ForegroundColor Green
Write-Host "`n仓库地址: https://github.com/$username/$repoName" -ForegroundColor Cyan
Write-Host "`n接下来你可以:" -ForegroundColor White
Write-Host "  1. 访问仓库页面查看代码" -ForegroundColor Gray
Write-Host "  2. 在 Settings → Secrets 里添加 OPENAI_API_KEY" -ForegroundColor Gray
Write-Host "  3. 用 GitHub Actions 或 Vercel 部署" -ForegroundColor Gray

Read-Host "`n按回车退出"
