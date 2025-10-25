# AI Camera SaaS - Stop Script for Windows
# PowerShell script to stop all services

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "AI Camera SaaS - Stopping Services" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker Compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    $dockerCompose = "docker compose"
} else {
    $dockerCompose = "docker-compose"
}

# Stop services
Write-Host "🛑 Stopping all services..." -ForegroundColor Yellow
try {
    Invoke-Expression "$dockerCompose down"

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ All services stopped successfully" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "⚠️  Some services may not have stopped properly" -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error stopping services: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "To remove volumes (delete all data):" -ForegroundColor Yellow
Write-Host "  $dockerCompose down -v" -ForegroundColor White
Write-Host ""
Write-Host "To start again:" -ForegroundColor Yellow
Write-Host "  .\start.ps1" -ForegroundColor White
Write-Host ""
