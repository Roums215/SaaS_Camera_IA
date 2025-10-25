# AI Camera SaaS - Logs Script for Windows
# PowerShell script to view logs

param(
    [string]$Service = "all",
    [switch]$Follow = $false
)

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "AI Camera SaaS - Service Logs" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker Compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    $dockerCompose = "docker compose"
} else {
    $dockerCompose = "docker-compose"
}

if ($Service -eq "all") {
    Write-Host "Showing logs for all services..." -ForegroundColor Yellow
    if ($Follow) {
        Write-Host "Press Ctrl+C to stop following logs" -ForegroundColor Gray
        Write-Host ""
        Invoke-Expression "$dockerCompose logs -f"
    } else {
        Invoke-Expression "$dockerCompose logs --tail=100"
    }
} else {
    Write-Host "Showing logs for $Service..." -ForegroundColor Yellow
    if ($Follow) {
        Write-Host "Press Ctrl+C to stop following logs" -ForegroundColor Gray
        Write-Host ""
        Invoke-Expression "$dockerCompose logs -f $Service"
    } else {
        Invoke-Expression "$dockerCompose logs --tail=100 $Service"
    }
}

Write-Host ""
Write-Host "Usage examples:" -ForegroundColor Yellow
Write-Host "  .\logs.ps1                  # View all logs (last 100 lines)" -ForegroundColor White
Write-Host "  .\logs.ps1 -Follow          # Follow all logs in real-time" -ForegroundColor White
Write-Host "  .\logs.ps1 -Service backend # View backend logs only" -ForegroundColor White
Write-Host "  .\logs.ps1 backend -Follow  # Follow backend logs" -ForegroundColor White
Write-Host ""
Write-Host "Available services:" -ForegroundColor Yellow
Write-Host "  backend, frontend, postgres, redis" -ForegroundColor White
Write-Host ""
