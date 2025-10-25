# AI Camera SaaS - Startup Script for Windows
# PowerShell script to start all services

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "AI Camera SaaS - Startup Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    pause
    exit 1
}

# Check if Docker is running
try {
    docker ps | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    pause
    exit 1
}

# Check if Docker Compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  docker-compose not found, using 'docker compose' instead" -ForegroundColor Yellow
    $dockerCompose = "docker compose"
} else {
    $dockerCompose = "docker-compose"
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "📝 Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Please edit .env file with your configuration before running in production!" -ForegroundColor Yellow
    Write-Host ""
}

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
$directories = @(
    "backend\models",
    "backend\uploads"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        New-Item -ItemType File -Path "$dir\.gitkeep" -Force | Out-Null
    }
}
Write-Host "✓ Directories created" -ForegroundColor Green

# Build and start services
Write-Host ""
Write-Host "🚀 Building and starting services..." -ForegroundColor Cyan
Write-Host "This may take a few minutes on first run..." -ForegroundColor Yellow
Write-Host ""

try {
    # Stop existing services
    Invoke-Expression "$dockerCompose down" 2>&1 | Out-Null

    # Build and start
    Invoke-Expression "$dockerCompose up -d --build"

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Services started successfully" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Failed to start services" -ForegroundColor Red
        Write-Host "Check the error messages above" -ForegroundColor Yellow
        pause
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error starting services: $_" -ForegroundColor Red
    pause
    exit 1
}

# Wait for services to be healthy
Write-Host ""
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
Invoke-Expression "$dockerCompose ps"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ Startup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Frontend:     " -NoNewline -ForegroundColor White
Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend API:  " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs:     " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Visit http://localhost:3000/register to create an account" -ForegroundColor White
Write-Host "2. Add a camera from the dashboard" -ForegroundColor White
Write-Host "3. For webcam: Source Type='webcam', Source='0'" -ForegroundColor White
Write-Host "4. Start the camera and view the live stream!" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop:      " -NoNewline -ForegroundColor White
Write-Host "$dockerCompose down" -ForegroundColor Yellow
Write-Host "📜 View logs:    " -NoNewline -ForegroundColor White
Write-Host "$dockerCompose logs -f" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to open the frontend in your browser..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open browser
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "✨ Enjoy your AI Camera SaaS!" -ForegroundColor Green
Write-Host ""
