# Quick Start Guide

Get your AI Camera SaaS up and running in minutes!

## Prerequisites

- **Docker** and **Docker Compose** installed
- A webcam or IP camera for testing
- 4GB+ RAM recommended

## 1. Installation (2 minutes)

```bash
# Clone or download the project
cd SaaS_Camera_IA

# Make start script executable
chmod +x start.sh

# Start the application
./start.sh
```

The script will:
- Create necessary directories
- Build Docker images
- Start all services (Backend, Frontend, PostgreSQL, Redis)

## 2. Create Your Account (1 minute)

1. Open your browser to http://localhost:3000
2. Click "Register"
3. Fill in:
   - Email: your@email.com
   - Username: admin
   - Password: (min 8 characters)
4. Click "Create account"

## 3. Add Your First Camera (1 minute)

1. Login with your credentials
2. Click the **"Add Camera"** button
3. Fill in:
   - **Name**: My Webcam
   - **Source Type**: webcam
   - **Source**: 0 (for default webcam)
4. Click **"Add Camera"**

## 4. Start Detection! (30 seconds)

1. Click **"Start"** button on your camera card
2. Click **"View Stream"** to see live detection
3. You should now see:
   - Live video from your webcam
   - Real-time object detection boxes
   - Confidence scores
   - Detection statistics

## Testing Shoplifting Detection

To test the AI detection:

1. **Position yourself** in front of the webcam
2. Make **suspicious movements**:
   - Reaching into pockets repeatedly
   - Looking around nervously
   - Concealing objects
3. Watch for **alerts** when suspicious behavior is detected
4. Check the **Alerts** page for notifications

## Camera Sources You Can Use

### Webcam (Easiest for Testing)
- **Source Type**: webcam
- **Source**: 0 (or 1, 2 for other cameras)

### IP Camera (RTSP)
- **Source Type**: rtsp
- **Source**: rtsp://username:password@192.168.1.100:554/stream

### HTTP Stream
- **Source Type**: http
- **Source**: http://192.168.1.100:8080/video

### Video File (For Testing)
- **Source Type**: file
- **Source**: /path/to/video.mp4

## Useful Commands

```bash
# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# View backend logs only
docker-compose logs -f backend

# View frontend logs only
docker-compose logs -f frontend

# Access database
docker exec -it ai_camera_postgres psql -U saas_camera_user -d saas_camera_db
```

## Key Features to Try

### 1. Dashboard
- **Location**: http://localhost:3000/dashboard
- View all cameras
- See detection statistics
- Manage camera status

### 2. Live Stream
- **Location**: Click "View Stream" on any camera
- Real-time video with AI detection
- Bounding boxes around detected objects
- Confidence scores
- Instant alerts for suspicious activity

### 3. Detections Page
- **Location**: http://localhost:3000/detections
- View all detection history
- Filter by confidence
- Filter by camera
- Review false positives

### 4. Alerts Page
- **Location**: http://localhost:3000/alerts
- See all security alerts
- Acknowledge alerts
- Resolve incidents
- View alert history

### 5. API Documentation
- **Location**: http://localhost:8000/docs
- Interactive Swagger UI
- Test all API endpoints
- See request/response schemas

## Troubleshooting

### Webcam Not Working?

**On Linux:**
```bash
# Check if webcam is available
ls -la /dev/video*

# Add your user to video group
sudo usermod -aG video $USER

# Restart your session
```

**On Docker:**
Make sure webcam device is mounted in docker-compose.yml:
```yaml
devices:
  - /dev/video0:/dev/video0
```

### Services Not Starting?

```bash
# Check if ports are already in use
netstat -tulpn | grep -E '3000|8000|5432|6379'

# Stop conflicting services or change ports in docker-compose.yml
```

### Database Issues?

```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

### Can't Connect to Backend?

1. Check backend is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Verify .env configuration
4. Ensure port 8000 is not blocked by firewall

## Performance Tips

### For Better Detection Speed:
1. Lower the FPS (15-20 fps is usually sufficient)
2. Reduce resolution (720p instead of 1080p)
3. Increase confidence threshold (0.6-0.7)

### For Better Accuracy:
1. Ensure good lighting
2. Position camera at optimal angle
3. Use higher resolution
4. Lower confidence threshold (0.4-0.5)

## Next Steps

1. **Customize Detection Settings**
   - Edit camera settings
   - Adjust confidence threshold
   - Set alert cooldown period

2. **Add More Cameras**
   - Monitor multiple locations
   - Different camera types
   - Mix webcams and IP cameras

3. **Review Analytics**
   - Check detection statistics
   - Analyze false positive rate
   - Monitor camera performance

4. **Set Up Production**
   - Configure SSL/TLS
   - Set up email notifications
   - Configure backup strategy
   - See full README.md for details

## Support

Need help?
- Check the full [README.md](README.md)
- Review API docs at http://localhost:8000/docs
- Check Docker logs: `docker-compose logs -f`

## Success Checklist

- [ ] Services started successfully
- [ ] Account created
- [ ] First camera added
- [ ] Camera started and streaming
- [ ] Detection working
- [ ] Can see live video feed
- [ ] Alerts appearing for detections
- [ ] Dashboard showing statistics

**If all checkboxes are complete, congratulations! Your AI Camera SaaS is fully operational!** 🎉

---

**Enjoy your production-ready AI security system!**
