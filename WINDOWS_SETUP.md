# Windows Setup Guide - AI Camera SaaS

Complete guide to install and run AI Camera SaaS on Windows.

## Prerequisites

### 1. Install Docker Desktop

1. Download Docker Desktop for Windows:
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"
   - Run the installer

2. During installation:
   - ✅ Enable WSL 2 (recommended)
   - ✅ Enable Hyper-V (if not using WSL 2)

3. After installation:
   - Restart your computer
   - Start Docker Desktop
   - Wait for Docker to start (whale icon in system tray)

### 2. Enable Webcam Access

1. Open Docker Desktop
2. Go to Settings (gear icon)
3. Navigate to Resources → Advanced
4. Ensure sufficient resources:
   - **CPUs**: 2 or more
   - **Memory**: 4 GB or more
   - **Disk**: 20 GB or more

### 3. Check Prerequisites

Open PowerShell and verify:

```powershell
# Check Docker
docker --version
# Should show: Docker version 20.x.x or higher

# Check Docker Compose
docker-compose --version
# Should show: Docker Compose version 2.x.x or higher
```

## Quick Start

### Method 1: Using PowerShell Scripts (Recommended)

1. **Open PowerShell as Administrator**
   - Right-click on PowerShell
   - Select "Run as Administrator"

2. **Navigate to project folder**
   ```powershell
   cd C:\path\to\SaaS_Camera_IA
   ```

3. **Enable script execution (first time only)**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Start the application**
   ```powershell
   .\start.ps1
   ```

5. **Access the application**
   - Browser will open automatically to http://localhost:3000
   - Or manually open: http://localhost:3000

### Method 2: Using Docker Compose Directly

```powershell
# Start services
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## Available PowerShell Scripts

### 🚀 start.ps1 - Start All Services
```powershell
.\start.ps1
```
- Creates necessary directories
- Builds Docker images
- Starts all services
- Opens browser automatically

### 🛑 stop.ps1 - Stop All Services
```powershell
.\stop.ps1
```
- Stops all running services
- Preserves data

### 🔄 restart.ps1 - Restart Services
```powershell
.\restart.ps1
```
- Restarts all services
- Useful after configuration changes

### 📜 logs.ps1 - View Logs
```powershell
# View all logs
.\logs.ps1

# Follow logs in real-time
.\logs.ps1 -Follow

# View specific service logs
.\logs.ps1 -Service backend
.\logs.ps1 -Service frontend
.\logs.ps1 -Service postgres
.\logs.ps1 -Service redis

# Follow specific service
.\logs.ps1 -Service backend -Follow
```

### 📊 status.ps1 - Check Status
```powershell
.\status.ps1
```
- Shows running containers
- Displays resource usage
- Shows access URLs

## Webcam Setup on Windows

### Finding Your Webcam

1. **Check Device Manager**
   - Press `Win + X`
   - Select "Device Manager"
   - Expand "Cameras" or "Imaging devices"
   - Note your camera name

2. **Test Webcam**
   - Open Camera app (built-in Windows app)
   - Verify camera works

### Adding Webcam to Application

1. **Access Frontend**
   - Open http://localhost:3000
   - Login or register

2. **Add Camera**
   - Click "Add Camera"
   - Fill in:
     - **Name**: "My Webcam"
     - **Source Type**: webcam
     - **Source**: 0

3. **Start Detection**
   - Click "Start" button
   - Click "View Stream"
   - You should see your webcam feed with AI detection

## Common Windows Issues

### Issue 1: PowerShell Script Won't Run

**Error**: "cannot be loaded because running scripts is disabled"

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 2: Docker Not Starting

**Solution**:
1. Open Docker Desktop
2. Wait for Docker to fully start (green icon)
3. Try again

### Issue 3: Port Already in Use

**Error**: "port is already allocated"

**Solution**:
```powershell
# Find process using port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill process (use PID from above)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Issue 4: WSL 2 Installation Required

**Solution**:
1. Open PowerShell as Administrator
2. Run:
   ```powershell
   wsl --install
   ```
3. Restart computer
4. Start Docker Desktop again

### Issue 5: Webcam Not Detected

**Windows Specific**:
Docker on Windows needs special configuration for webcam access.

**Alternative Solution**:
Use the browser's webcam API:
1. The frontend can access webcam directly through browser
2. Upload video to backend for processing
3. Or use IP camera (RTSP stream)

### Issue 6: Hyper-V Not Available

**Solution**:
1. Enable WSL 2 instead (recommended)
2. Or enable Hyper-V:
   ```powershell
   # Run as Administrator
   Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
   ```
3. Restart computer

## Firewall Configuration

If you can't access the application:

1. **Open Windows Defender Firewall**
   - Search for "Windows Defender Firewall"
   - Click "Allow an app through firewall"

2. **Add Docker**
   - Click "Change settings"
   - Find "Docker Desktop" and check both Private and Public
   - Click OK

3. **Or Create Rule**
   ```powershell
   # Run as Administrator
   New-NetFirewallRule -DisplayName "AI Camera Frontend" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
   New-NetFirewallRule -DisplayName "AI Camera Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

## Performance Optimization

### For Better Performance on Windows:

1. **Increase Docker Resources**
   - Open Docker Desktop Settings
   - Resources → Advanced
   - Increase CPUs to 4
   - Increase Memory to 6 GB

2. **Use WSL 2**
   - Better performance than Hyper-V
   - More efficient file system

3. **Disable Unnecessary Services**
   ```powershell
   # Stop Redis if not using caching
   docker-compose stop redis
   ```

4. **Lower Detection Quality**
   - In camera settings:
     - Lower FPS (15-20)
     - Lower resolution (720p)
     - Increase confidence threshold

## Useful Commands

```powershell
# Check Docker status
docker ps

# Stop all containers
docker-compose down

# Remove all data and start fresh
docker-compose down -v
.\start.ps1

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Restart specific service
docker-compose restart backend

# Access database
docker exec -it ai_camera_postgres psql -U saas_camera_user -d saas_camera_db

# Clean up Docker
docker system prune -a

# Check resource usage
docker stats
```

## Accessing from Other Devices

To access from other devices on your network:

1. **Find Your IP Address**
   ```powershell
   ipconfig
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. **Update CORS Settings**
   - Edit `.env` file
   - Add your IP to `BACKEND_CORS_ORIGINS`
   ```
   BACKEND_CORS_ORIGINS=["http://localhost:3000","http://192.168.1.100:3000"]
   ```

3. **Access from Other Device**
   - Open browser on another device
   - Go to: http://192.168.1.100:3000

## Backup and Restore

### Backup Database

```powershell
# Backup
docker exec ai_camera_postgres pg_dump -U saas_camera_user saas_camera_db > backup.sql

# Restore
Get-Content backup.sql | docker exec -i ai_camera_postgres psql -U saas_camera_user -d saas_camera_db
```

### Backup Configuration

```powershell
# Copy important files
Copy-Item .env backup\.env
Copy-Item docker-compose.yml backup\docker-compose.yml
```

## Uninstallation

To completely remove the application:

```powershell
# Stop and remove containers
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Remove project folder
Remove-Item -Recurse -Force C:\path\to\SaaS_Camera_IA
```

## Next Steps

After successful installation:

1. ✅ Create an account at http://localhost:3000/register
2. ✅ Add your webcam as a camera source
3. ✅ Start detection and view live stream
4. ✅ Check alerts and detection history
5. ✅ Explore API documentation at http://localhost:8000/docs

## Support

If you encounter issues:

1. Check logs: `.\logs.ps1 -Follow`
2. Check status: `.\status.ps1`
3. Restart services: `.\restart.ps1`
4. Review Docker Desktop logs
5. Check Windows Event Viewer

## Video Tutorial

For a visual guide, check the README.md for screenshots and detailed explanations.

---

**Ready to start? Run `.\start.ps1` and your AI Camera SaaS will be up in minutes!** 🚀
