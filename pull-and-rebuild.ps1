# AI Camera SaaS - Pull and Rebuild Script for Windows
# PowerShell script to pull latest changes and rebuild

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "AI Camera SaaS - Pull and Rebuild" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker Compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    $dockerCompose = "docker compose"
} else {
    $dockerCompose = "docker-compose"
}

# Stop current services
Write-Host "Stopping current services..." -ForegroundColor Yellow
Invoke-Expression "$dockerCompose down"

# Pull latest changes from Git
Write-Host ""
Write-Host "Pulling latest changes from Git..." -ForegroundColor Yellow
git pull origin claude/ai-camera-saas-011CUUHdstKnZTdkeiYhBwhp

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[X] Failed to pull changes. Check if you have uncommitted changes." -ForegroundColor Red
    Write-Host ""
    Write-Host "To force update:" -ForegroundColor Yellow
    Write-Host "  git fetch origin" -ForegroundColor White
    Write-Host "  git reset --hard origin/claude/ai-camera-saas-011CUUHdstKnZTdkeiYhBwhp" -ForegroundColor White
    pause
    exit 1
}

Write-Host "[OK] Latest changes pulled" -ForegroundColor Green

# Remove old images to force rebuild
Write-Host ""
Write-Host "Removing old Docker images..." -ForegroundColor Yellow
docker rmi saas_camera_ia-backend -f 2>$null
docker rmi saas_camera_ia-frontend -f 2>$null

# Rebuild and start
Write-Host ""
Write-Host "Rebuilding services (this may take a few minutes)..." -ForegroundColor Cyan
Invoke-Expression "$dockerCompose build --no-cache"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Build successful!" -ForegroundColor Green

    Write-Host ""
    Write-Host "Starting services..." -ForegroundColor Yellow
    Invoke-Expression "$dockerCompose up -d"

    Write-Host ""
    Write-Host "[OK] Services started!" -ForegroundColor Green

    # Wait for services
    Write-Host ""
    Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10

    # Show status
    Write-Host ""
    Invoke-Expression "$dockerCompose ps"

    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host "Ready!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Frontend:     http://localhost:3000" -ForegroundColor Cyan
    Write-Host "Backend API:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""

    # Open browser
    Write-Host "Opening browser..." -ForegroundColor Yellow
    Start-Process "http://localhost:3000"

} else {
    Write-Host ""
    Write-Host "[X] Build failed. Check error messages above." -ForegroundColor Red
    pause
}

Write-Host ""
