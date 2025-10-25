# AI Camera SaaS - Status Script for Windows
# PowerShell script to check service status

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "AI Camera SaaS - Service Status" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker Compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    $dockerCompose = "docker compose"
} else {
    $dockerCompose = "docker-compose"
}

# Get service status
Write-Host "📊 Checking service status..." -ForegroundColor Yellow
Write-Host ""

try {
    Invoke-Expression "$dockerCompose ps"

    Write-Host ""
    Write-Host "🌐 Access Points:" -ForegroundColor Cyan
    Write-Host "  Frontend:     http://localhost:3000" -ForegroundColor White
    Write-Host "  Backend API:  http://localhost:8000" -ForegroundColor White
    Write-Host "  API Docs:     http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""

    # Check if services are running
    $runningServices = docker ps --filter "name=ai_camera" --format "{{.Names}}" 2>$null

    if ($runningServices) {
        Write-Host "✓ Services are running" -ForegroundColor Green
        Write-Host ""
        Write-Host "Running containers:" -ForegroundColor Yellow
        $runningServices | ForEach-Object {
            Write-Host "  • $_" -ForegroundColor White
        }
    } else {
        Write-Host "⚠️  No services are running" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "To start services:" -ForegroundColor Yellow
        Write-Host "  .\start.ps1" -ForegroundColor White
    }

    Write-Host ""

    # Show resource usage
    Write-Host "💻 Resource Usage:" -ForegroundColor Cyan
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" --filter "name=ai_camera" 2>$null

} catch {
    Write-Host "❌ Error checking status: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure Docker is running" -ForegroundColor Yellow
}

Write-Host ""
