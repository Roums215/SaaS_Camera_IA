#!/bin/bash

echo "========================================="
echo "AI Camera SaaS - Startup Script"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before running in production!"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/models backend/uploads
touch backend/models/.gitkeep backend/uploads/.gitkeep

# Build and start services
echo ""
echo "🚀 Building and starting services..."
echo ""
docker-compose up -d --build

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "========================================="
echo "✅ Startup Complete!"
echo "========================================="
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📖 Next Steps:"
echo "1. Visit http://localhost:3000/register to create an account"
echo "2. Add a camera from the dashboard"
echo "3. For webcam: Source Type='webcam', Source='0'"
echo "4. Start the camera and view the live stream!"
echo ""
echo "🛑 To stop: docker-compose down"
echo "📜 View logs: docker-compose logs -f"
echo ""
