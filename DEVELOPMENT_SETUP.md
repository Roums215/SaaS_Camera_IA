# Development Setup Guide

This guide explains how to run the AI Camera SaaS application in different development modes.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start (Docker - Recommended)](#quick-start-docker---recommended)
- [Local Development Mode](#local-development-mode)
- [Hybrid Development Mode](#hybrid-development-mode)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### For Docker Mode
- Docker and Docker Compose installed
- Webcam or IP camera (for testing)

### For Local Development Mode
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Webcam or IP camera (for testing)

## Quick Start (Docker - Recommended)

This mode runs all services (frontend, backend, database, Redis) in Docker containers.

### Linux / macOS
```bash
./start.sh
```

### Windows
```powershell
.\start.ps1
```

### Manual Docker Start
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Local Development Mode

This mode runs all services directly on your machine (no Docker). This is useful for rapid development and debugging.

### Step 1: Set Up PostgreSQL

Install PostgreSQL 15+ and create the database:

```bash
# Create database and user
psql -U postgres
CREATE DATABASE saas_camera_db;
CREATE USER saas_camera_user WITH PASSWORD 'saas_camera_password_2024';
GRANT ALL PRIVILEGES ON DATABASE saas_camera_db TO saas_camera_user;
\q
```

### Step 2: Set Up Redis

Install and start Redis:

```bash
# Linux/macOS
redis-server

# Windows (using WSL or Redis installer)
redis-server.exe
```

### Step 3: Set Up Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify .env file exists
# The .env file should already be created with local settings
cat .env  # Linux/macOS
type .env  # Windows

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000

### Step 4: Set Up Frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Verify .env file exists
cat .env  # Linux/macOS
type .env  # Windows

# Start the development server
npm run dev
```

The frontend will be available at http://localhost:5173 (Vite dev server)

## Hybrid Development Mode

This mode is useful when you want to run some services in Docker and others locally.

### Option 1: Backend Local, Database/Redis in Docker

Start only database and Redis:
```bash
docker-compose up -d postgres redis
```

Then follow [Step 3](#step-3-set-up-backend) and [Step 4](#step-4-set-up-frontend) above.

### Option 2: Frontend Local, Backend in Docker

Start backend with its dependencies:
```bash
docker-compose up -d postgres redis backend
```

Then follow [Step 4](#step-4-set-up-frontend) for the frontend.

## Environment Configuration

### Backend .env

The backend `.env` file is already configured for local development:

```bash
# Key settings for local development
POSTGRES_SERVER=localhost        # Use 'postgres' for Docker
REDIS_HOST=localhost             # Use 'redis' for Docker
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:8000"]
```

**Important:**
- For local dev: Use `localhost` for database and Redis
- For Docker: Use service names (`postgres`, `redis`)

### Frontend .env

The frontend `.env` file is configured to connect to the backend:

```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/api/v1/ws
```

These URLs work for both:
- Backend running locally
- Backend running in Docker (exposed on port 8000)

## Troubleshooting

### Authentication Errors (ERR_EMPTY_RESPONSE)

**Problem:** Frontend shows `ERR_EMPTY_RESPONSE` when trying to login/register

**Solution:**
1. Verify backend is running:
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy","app":"AI Camera SaaS","version":"1.0.0"}`

2. Check backend logs:
   ```bash
   # Docker mode
   docker-compose logs backend

   # Local mode
   # Check the terminal where uvicorn is running
   ```

3. Verify .env files exist:
   ```bash
   ls backend/.env
   ls frontend/.env
   ```

### CORS Errors

**Problem:** Browser console shows CORS errors

**Solution:**
1. Verify `BACKEND_CORS_ORIGINS` in backend `.env` includes your frontend URL:
   - http://localhost:5173 (Vite dev server)
   - http://localhost:3000 (production build)

2. Restart the backend after changing CORS settings

### Database Connection Errors

**Problem:** Backend fails to start with database connection errors

**Solution:**

For **Docker mode**:
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

For **Local mode**:
```bash
# Verify PostgreSQL is running
pg_isready -h localhost -p 5432

# Check if database exists
psql -U postgres -c "\l" | grep saas_camera_db

# Verify credentials in backend/.env match your PostgreSQL setup
```

### Redis Connection Errors

**Problem:** Backend logs show Redis connection errors

**Solution:**

For **Docker mode**:
```bash
# Check if Redis is running
docker-compose ps redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

For **Local mode**:
```bash
# Verify Redis is running
redis-cli ping
# Should return: PONG
```

### Port Already in Use

**Problem:** Cannot start service because port is already in use

**Solution:**
```bash
# Find process using the port (Linux/macOS)
lsof -i :8000  # Backend
lsof -i :3000  # Frontend production
lsof -i :5173  # Frontend dev

# Find process using the port (Windows)
netstat -ano | findstr :8000

# Kill the process or use different ports
```

### Model Loading Errors

**Problem:** Backend fails to load AI model

**Solution:**
1. The default model path is `./models/yolov8n.pt`
2. YOLOv8 will auto-download the model on first run
3. Ensure the backend has internet access for the initial download
4. Check the `MODEL_PATH` in backend `.env`

### Vite Dev Server Not Starting

**Problem:** Frontend fails to start with `npm run dev`

**Solution:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite

# Try starting again
npm run dev
```

## Development Workflow

### Making Changes

1. **Backend changes:**
   - Edit Python files in `backend/app/`
   - Uvicorn auto-reloads on file changes (when using `--reload` flag)

2. **Frontend changes:**
   - Edit files in `frontend/src/`
   - Vite hot-reloads automatically

3. **Database schema changes:**
   ```bash
   cd backend

   # Create a new migration
   alembic revision --autogenerate -m "description of changes"

   # Apply migrations
   alembic upgrade head
   ```

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test

# Build frontend
npm run build
npm run preview
```

## First Time Setup

After starting the application:

1. **Register an account:**
   - Navigate to http://localhost:5173/register (dev) or http://localhost:3000/register (Docker)
   - Create your admin account

2. **Add your first camera:**
   - Click "Add Camera" on the dashboard
   - For webcam testing:
     - Name: "My Webcam"
     - Source Type: "webcam"
     - Source: "0" (default webcam)

3. **Start detection:**
   - Click "Start" on your camera card
   - Click "View Stream" to see live detection

## Additional Resources

- [README.md](README.md) - Main project documentation
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when backend is running)
- [WINDOWS_SETUP.md](WINDOWS_SETUP.md) - Windows-specific setup instructions

---

**Need help?** Check the [Troubleshooting](#troubleshooting) section or create an issue on GitHub.
