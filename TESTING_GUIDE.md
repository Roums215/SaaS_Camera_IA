# Testing Guide - AI Camera SaaS

Complete guide to test your AI Camera SaaS with your PC webcam.

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Docker and Docker Compose installed
- [ ] Webcam connected and working
- [ ] Ports 3000, 8000, 5432, 6379 available
- [ ] At least 4GB RAM available
- [ ] Good lighting for camera detection

## Step-by-Step Testing

### Step 1: Start the Application (2 minutes)

```bash
cd SaaS_Camera_IA

# Start all services
./start.sh
```

**Expected Output:**
```
✅ Startup Complete!
🌐 Frontend: http://localhost:3000
🔧 Backend API: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
```

**Verify Services:**
```bash
docker-compose ps
```

All services should be "Up" and healthy.

### Step 2: Create Your Account (1 minute)

1. Open browser: http://localhost:3000
2. Click **"Register"**
3. Fill the form:
   - Email: `test@example.com`
   - Username: `testuser`
   - Password: `testpass123`
4. Click **"Create account"**
5. You'll be redirected to login page

### Step 3: Login (30 seconds)

1. Enter credentials:
   - Username: `testuser`
   - Password: `testpass123`
2. Click **"Sign in"**
3. You should see the Dashboard

### Step 4: Add Webcam (1 minute)

1. Click **"Add Camera"** button
2. Fill the form:
   - **Name**: `My Test Webcam`
   - **Source Type**: Select `webcam`
   - **Source**: Enter `0`
3. Click **"Add Camera"**
4. Camera card appears on dashboard

### Step 5: Start Detection (30 seconds)

1. Find your camera card
2. Click the **▶ Play** button (Start)
3. Wait 2-3 seconds
4. Status should change to **"Active"**

### Step 6: View Live Stream (Immediate)

1. Click **"View Stream"** on your camera card
2. You should see:
   - ✅ Live video from your webcam
   - ✅ Green "Connected" status indicator
   - ✅ Detection boxes (if people/objects in view)
   - ✅ Confidence scores
   - ✅ Statistics on the right sidebar

## What to Test

### 1. Real-Time Detection

**Test Scenario: Person Detection**
1. Position yourself in front of the webcam
2. Wait 1-2 seconds
3. **Expected**: Green box around you with "person" label
4. **Check**: Confidence score (should be >50%)

**Test Scenario: Multiple Objects**
1. Show different objects to the camera
2. Move around slowly
3. **Expected**: Detection boxes update in real-time
4. **Check**: Detection count in top-right corner

### 2. Suspicious Activity Alert

**Test Scenario: Trigger Alert**
1. Make suspicious movements:
   - Reach into pockets repeatedly
   - Look around nervously
   - Make sudden movements
2. **Expected**: Red "SUSPICIOUS ACTIVITY DETECTED" banner
3. **Check**: Alert appears in Alerts page

**Verify Alert:**
1. Click **"Alerts"** in navigation
2. **Expected**: New alert with "High" or "Critical" severity
3. Try clicking **"Acknowledge"** button
4. Try clicking **"Resolve"** button

### 3. Detection History

**Check Detections Page:**
1. Click **"Detections"** in navigation
2. **Expected**: List of all detections
3. **Check**: Each detection shows:
   - Camera ID
   - Detection type
   - Confidence score
   - Timestamp

**Test Filters:**
1. Adjust **"Min Confidence"** slider
2. **Expected**: Detections update based on confidence
3. Enter camera ID in filter
4. **Expected**: Only that camera's detections shown

### 4. Dashboard Statistics

**Check Stats:**
1. Go back to Dashboard
2. **Expected Stats Cards**:
   - Total Detections (7d)
   - Average Confidence
   - False Positives
   - Active Cameras

**Verify Updates:**
1. Trigger more detections (wave at camera)
2. Refresh page
3. **Expected**: Stats increase

### 5. Camera Controls

**Test Start/Stop:**
1. Click **■ Stop** button on camera
2. **Expected**: Status changes to "Inactive"
3. Stream page shows "Waiting for stream..."
4. Click **▶ Start** again
5. **Expected**: Stream resumes

### 6. WebSocket Connection

**Test Real-Time Updates:**
1. Open stream page
2. Open browser console (F12)
3. Look for WebSocket messages
4. **Expected**: "WebSocket connected" message
5. **Check**: Frame updates every second

### 7. Camera Settings

**View Camera Stats:**
1. On stream page, check right sidebar
2. **Expected Information**:
   - Camera status
   - Source type
   - Resolution
   - FPS
   - Confidence threshold
   - Total detections
   - Detections today

## Performance Testing

### CPU Usage Test
```bash
# Monitor CPU usage
docker stats
```
**Expected**: Backend CPU < 50% during streaming

### Memory Usage Test
**Expected**:
- Backend: < 500MB
- Frontend: < 200MB
- PostgreSQL: < 100MB
- Redis: < 50MB

### Frame Rate Test
1. Watch live stream
2. **Expected**: Smooth video (15-30 fps)
3. No significant lag (< 1 second)

## Common Issues & Solutions

### Issue: Webcam Not Detected

**Solution 1: Check Device**
```bash
# Linux: List video devices
ls -la /dev/video*

# Should show: /dev/video0
```

**Solution 2: Docker Permissions**
```bash
# Add user to video group
sudo usermod -aG video $USER

# Restart Docker
sudo systemctl restart docker
```

**Solution 3: Check Docker Compose**
Ensure docker-compose.yml has:
```yaml
devices:
  - /dev/video0:/dev/video0
privileged: true
```

### Issue: No Detection Boxes

**Possible Causes:**
1. Low confidence threshold
2. Poor lighting
3. Objects too small/far

**Solutions:**
1. Adjust confidence: Edit camera settings → Lower threshold to 0.3
2. Improve lighting: Add more light
3. Move closer to camera

### Issue: WebSocket Connection Failed

**Check Backend:**
```bash
docker-compose logs backend | grep -i websocket
```

**Check Token:**
1. Open browser console
2. Check WebSocket URL includes token
3. Token should be in URL: `?token=...`

### Issue: Alerts Not Appearing

**Verify:**
1. Check detection is marked as suspicious
2. Look for "has_suspicious_activity": true in console
3. Check Alerts page directly

### Issue: Slow Performance

**Optimize:**
1. Lower FPS: Edit camera → Set FPS to 15
2. Lower resolution: Set to 720p
3. Increase confidence: Set threshold to 0.6

## API Testing

### Test with cURL

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

**Get Cameras:**
```bash
TOKEN="your-token-here"
curl http://localhost:8000/api/v1/cameras/ \
  -H "Authorization: Bearer $TOKEN"
```

**Get Detections:**
```bash
curl http://localhost:8000/api/v1/detections/ \
  -H "Authorization: Bearer $TOKEN"
```

### Interactive API Testing

Visit: http://localhost:8000/docs

1. Click **"Authorize"** button
2. Enter your token
3. Try different endpoints
4. See request/response examples

## Advanced Testing

### Test RTSP Stream (If Available)

```bash
# Add RTSP camera
Name: "IP Camera"
Source Type: rtsp
Source: rtsp://username:password@192.168.1.100:554/stream
```

### Test Multiple Cameras

1. Add 2-3 different cameras
2. Start all cameras
3. Open multiple stream tabs
4. **Expected**: All streams work simultaneously

### Test Different Users

1. Logout
2. Register new user
3. Login as new user
4. **Expected**: Empty dashboard (no cameras from other users)

### Stress Test

1. Open 5+ browser tabs
2. All viewing same stream
3. **Expected**: System remains responsive
4. Check CPU usage

## Validation Checklist

After testing, verify:

- [ ] Can register and login
- [ ] Can add webcam camera
- [ ] Can start/stop camera
- [ ] Live stream displays video
- [ ] Detections appear in real-time
- [ ] Detection boxes are accurate
- [ ] Confidence scores make sense
- [ ] Alerts are created for suspicious activity
- [ ] Can acknowledge/resolve alerts
- [ ] Dashboard stats update
- [ ] Detections page shows history
- [ ] Filters work on detections page
- [ ] WebSocket connection stable
- [ ] No console errors
- [ ] API documentation accessible
- [ ] Can logout successfully

## Test Results Template

```
Test Date: ___________
Tester: ___________

✅ User Registration: PASS/FAIL
✅ User Login: PASS/FAIL
✅ Add Camera: PASS/FAIL
✅ Start Camera: PASS/FAIL
✅ Live Stream: PASS/FAIL
✅ Real-time Detection: PASS/FAIL
✅ Alert Generation: PASS/FAIL
✅ Alert Management: PASS/FAIL
✅ Detection History: PASS/FAIL
✅ Dashboard Stats: PASS/FAIL
✅ Camera Controls: PASS/FAIL
✅ WebSocket Connection: PASS/FAIL

Performance:
- CPU Usage: ____%
- Memory Usage: ____MB
- Frame Rate: ____fps
- Response Time: ____ms

Issues Found:
1. ___________
2. ___________
3. ___________

Overall Rating: ⭐⭐⭐⭐⭐
```

## Debug Mode

Enable debug logs:

**Backend:**
```bash
# In docker-compose.yml
environment:
  - DEBUG=True

# Restart
docker-compose restart backend
```

**View Logs:**
```bash
# All logs
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

## Cleanup After Testing

```bash
# Stop all services
docker-compose down

# Remove volumes (fresh start)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Next Steps After Successful Testing

1. ✅ **Production Deployment**
   - Update environment variables
   - Set up SSL/TLS
   - Configure domain name

2. ✅ **Monitoring Setup**
   - Add Prometheus
   - Set up Grafana dashboards
   - Configure alerts

3. ✅ **Backup Strategy**
   - Database backups
   - Configuration backups
   - Video storage strategy

4. ✅ **Security Hardening**
   - Change default passwords
   - Enable rate limiting
   - Set up firewall rules

---

**Congratulations! Your AI Camera SaaS is fully tested and ready for use! 🎉**
