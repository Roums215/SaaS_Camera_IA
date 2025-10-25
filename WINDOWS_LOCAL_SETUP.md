# Windows Local Development Setup

This guide is specifically for Windows users who want to run the AI Camera SaaS application locally (not in Docker).

## Prerequisites

- Python 3.11 or 3.12 installed
- Node.js 18+ installed
- Docker Desktop for Windows (for PostgreSQL and Redis)
- PowerShell or Command Prompt

## Quick Start

The easiest way on Windows is to use Docker for the databases and run the application locally:

### Step 1: Start Databases in Docker

Open PowerShell and run:

```powershell
cd C:\path\to\SaaS_Camera_IA
docker-compose up -d postgres redis
```

Wait for the services to be healthy (about 30-60 seconds).

### Step 2: Set Up Backend

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative for Command Prompt:
# venv\Scripts\activate.bat

# Upgrade pip (recommended)
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create database tables
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend should now be running at http://localhost:8000

### Step 3: Set Up Frontend

Open a **NEW** PowerShell window:

```powershell
# Navigate to frontend directory
cd C:\path\to\SaaS_Camera_IA\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend should now be running at http://localhost:5173

## Common Windows Issues and Solutions

### Issue 1: "source: command not found"

**Problem:** You used the Linux/Mac command `source` in PowerShell

**Solution:** Use the Windows activation command:

```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate.bat
```

### Issue 2: Script Execution Policy Error

**Problem:**
```
cannot be loaded because running scripts is disabled on this system
```

**Solution:**

```powershell
# Run this once in PowerShell as Administrator or current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating the virtual environment again.

### Issue 3: torch==2.1.2 Not Available for Python 3.12

**Problem:**
```
ERROR: Could not find a version that satisfies the requirement torch==2.1.2
```

**Solution:** This has been fixed in the updated `requirements.txt`. The file now uses `torch>=2.2.0` which supports Python 3.12.

If you still see this error:
1. Make sure you pulled the latest changes
2. Delete the venv and recreate it:
   ```powershell
   Remove-Item -Recurse -Force venv
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

### Issue 4: Commands Not Found (alembic, uvicorn, etc.)

**Problem:**
```
alembic: The term 'alembic' is not recognized...
uvicorn: The term 'uvicorn' is not recognized...
```

**Solution:** The virtual environment is not activated. You'll see `(venv)` in your prompt when it's activated:

```powershell
# Should show (venv) before your prompt
(venv) PS C:\...\backend>
```

If you don't see `(venv)`, activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### Issue 5: PostgreSQL Connection Error

**Problem:**
```
could not connect to server: Connection refused
```

**Solution:**

1. Check if Docker containers are running:
   ```powershell
   docker ps
   ```
   You should see `ai_camera_postgres` and `ai_camera_redis` with status "Up"

2. If not running, start them:
   ```powershell
   docker-compose up -d postgres redis
   ```

3. Wait 30 seconds for them to be healthy, then check:
   ```powershell
   docker ps
   ```

### Issue 6: Port Already in Use

**Problem:**
```
Error: Port 8000 is already in use
```

**Solution:**

Find and kill the process using the port:

```powershell
# Find process ID using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the actual number)
taskkill /PID <PID> /F
```

Or use a different port:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Don't forget to update `frontend/.env` if you change the backend port.

### Issue 7: Cannot Import cv2 (OpenCV)

**Problem:**
```
ImportError: DLL load failed while importing cv2
```

**Solution:**

Install Visual C++ Redistributable:
1. Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Install it
3. Restart your terminal
4. Try running the backend again

### Issue 8: Database Tables Not Created

**Problem:** Backend starts but you get errors about missing tables

**Solution:**

Make sure you ran the migrations:

```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Run migrations
alembic upgrade head
```

## Checking Your Setup

### 1. Check Python Version

```powershell
python --version
# Should show Python 3.11.x or 3.12.x
```

### 2. Check Virtual Environment

```powershell
# Your prompt should show (venv)
(venv) PS C:\...\backend>

# Check where Python is running from
where.exe python
# Should show path in venv folder
```

### 3. Check Backend Health

```powershell
# In a new PowerShell window
curl http://localhost:8000/health

# Or in browser, visit: http://localhost:8000/health
```

Should return:
```json
{"status":"healthy","app":"AI Camera SaaS","version":"1.0.0"}
```

### 4. Check Database Connection

```powershell
docker exec -it ai_camera_postgres psql -U saas_camera_user -d saas_camera_db -c "SELECT 1;"

# Should return:
#  ?column?
# ----------
#         1
```

### 5. Check Redis Connection

```powershell
docker exec -it ai_camera_redis redis-cli ping

# Should return: PONG
```

## Alternative: Full Docker Mode

If local development is too problematic, use full Docker mode instead:

```powershell
# Stop local services if running (Ctrl+C in terminals)

# Stop only databases
docker-compose down

# Start all services in Docker
docker-compose up -d

# Wait for services to start (about 2 minutes)

# Check logs
docker-compose logs -f
```

Then access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development Workflow

### Starting Work Each Day

```powershell
# Terminal 1 - Databases (if not running)
docker-compose up -d postgres redis

# Terminal 2 - Backend
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Terminal 3 - Frontend
cd frontend
npm run dev
```

### Stopping Everything

```powershell
# Stop backend/frontend: Ctrl+C in each terminal

# Stop databases
docker-compose down
```

### Making Database Changes

```powershell
cd backend
.\venv\Scripts\Activate.ps1

# Create migration
alembic revision --autogenerate -m "describe your changes"

# Apply migration
alembic upgrade head
```

## Troubleshooting Tips

1. **Always activate the virtual environment** before running Python commands
2. **Check Docker Desktop** is running before starting databases
3. **Use PowerShell** (not Command Prompt) for better compatibility
4. **Check the logs** if something doesn't work:
   ```powershell
   docker-compose logs postgres
   docker-compose logs redis
   ```
5. **Restart your terminal** after installing new software

## Getting Help

- See [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md) for general development info
- See [README.md](README.md) for project overview
- Check the [Troubleshooting section](#common-windows-issues-and-solutions) above
- Create an issue on GitHub if you're still stuck

## VS Code Setup (Optional)

If you use VS Code:

1. Install Python extension
2. Select the virtual environment:
   - `Ctrl+Shift+P`
   - Type: "Python: Select Interpreter"
   - Choose: `.\venv\Scripts\python.exe`

3. Recommended extensions:
   - Python
   - Pylance
   - Python Debugger
   - ESLint (for frontend)
   - Prettier (for frontend)

---

**Need more help?** Check the main [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md) or create an issue.
