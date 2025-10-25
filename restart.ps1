# AI Camera SaaS - Restart Script for Windows
# PowerShell script to restart all services

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "AI Camera SaaS - Restarting Services" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker Compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    $dockerCompose = "docker compose"
} else {
    $dockerCompose = "docker-compose"
}

# Restart services
Write-Host "🔄 Restarting all services..." -ForegroundColor Yellow
try {
    Invoke-Expression "$dockerCompose restart"

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ All services restarted successfully" -ForegroundColor Green

        # Wait for services to be ready
        Write-Host ""
        Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5

        # Check status
        Write-Host ""
        Write-Host "📊 Service Status:" -ForegroundColor Cyan
        Invoke-Expression "$dockerCompose ps"

        Write-Host ""
        Write-Host "🌐 Frontend:     http://localhost:3000" -ForegroundColor Cyan
        Write-Host "🔧 Backend API:  http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📚 API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "⚠️  Some services may not have restarted properly" -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error restarting services: $_" -ForegroundColor Red
}

Write-Host ""
