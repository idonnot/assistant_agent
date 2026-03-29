# Windows PowerShell启动脚本
# 用法:.\start-dev.ps1

Write-Host "🚀 启动Weather Agent系统..." -ForegroundColor Green
Write-Host ""

# 检查Node.js
Write-Host "检查Node.js..." -ForegroundColor Yellow
if (!(Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js未安装或未添加到PATH" -ForegroundColor Red
    Write-Host "请访问 https://nodejs.org/ 下载安装" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Node.js已安装: $(node --version)" -ForegroundColor Green
Write-Host ""

# 启动Elasticsearch
Write-Host "1️⃣  启动Elasticsearch..." -ForegroundColor Yellow
docker-compose -f docker/docker-compose.yml up -d elasticsearch
Start-Sleep -Seconds 10

# 启动后端
Write-Host "2️⃣  启动FastAPI后端..." -ForegroundColor Yellow
Write-Host "在新窗口启动: 请运行以下命令" -ForegroundColor Cyan
Write-Host "cd backend && pip install -r requirements.txt && python -m uvicorn main:app --reload --port 8000" -ForegroundColor Cyan
Write-Host ""

# 启动前端
Write-Host "3️⃣  启动React前端..." -ForegroundColor Yellow
cd frontend
npm install
npm run dev
