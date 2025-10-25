# AI Camera SaaS - Shoplifting Detection System

A production-ready SaaS platform for real-time shoplifting detection using YOLOv8 AI model. Monitor multiple cameras, detect suspicious behavior, and receive instant alerts.

## Features

- **Real-time Video Streaming**: WebSocket-based live camera feeds with AI detection
- **YOLOv8 Detection**: Advanced object detection and suspicious behavior identification
- **Multi-camera Support**: Manage unlimited cameras (webcam, RTSP, HTTP streams)
- **Instant Alerts**: Real-time notifications for suspicious activities
- **User Authentication**: Secure JWT-based authentication system
- **Analytics Dashboard**: Comprehensive statistics and detection history
- **RESTful API**: Full-featured API with Swagger documentation
- **Docker Support**: Easy deployment with Docker Compose
- **Production Ready**: Built with FastAPI, React, PostgreSQL, and Redis

## Technology Stack

### Backend
- **FastAPI**: High-performance async Python framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **Redis**: Caching and real-time features
- **YOLOv8**: State-of-the-art object detection
- **OpenCV**: Computer vision processing
- **WebSocket**: Real-time video streaming

### Frontend
- **React 18**: Modern UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool
- **TailwindCSS**: Utility-first CSS framework
- **React Query**: Data fetching and caching
- **Zustand**: State management
- **React Router**: Navigation

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)
- Webcam or IP camera (for testing)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SaaS_Camera_IA
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### First Time Setup

1. **Register an account**
   - Navigate to http://localhost:3000/register
   - Create your admin account

2. **Add your first camera**
   - Click "Add Camera" on the dashboard
   - For webcam testing, use:
     - Name: "My Webcam"
     - Source Type: "webcam"
     - Source: "0" (default webcam)

3. **Start detection**
   - Click "Start" on your camera card
   - Click "View Stream" to see live detection

## Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
alembic upgrade head

# Run development server
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Project Structure

```
SaaS_Camera_IA/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── stores/       # State management
│   │   ├── hooks/        # Custom hooks
│   │   └── types/        # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Main Endpoints

- **Authentication**
  - `POST /api/v1/auth/register` - Register new user
  - `POST /api/v1/auth/login` - Login
  - `GET /api/v1/auth/me` - Get current user

- **Cameras**
  - `GET /api/v1/cameras/` - List cameras
  - `POST /api/v1/cameras/` - Create camera
  - `GET /api/v1/cameras/{id}` - Get camera details
  - `POST /api/v1/cameras/{id}/start` - Start camera
  - `POST /api/v1/cameras/{id}/stop` - Stop camera

- **Detections**
  - `GET /api/v1/detections/` - List detections
  - `GET /api/v1/detections/stats/summary` - Detection statistics

- **Alerts**
  - `GET /api/v1/alerts/` - List alerts
  - `POST /api/v1/alerts/{id}/acknowledge` - Acknowledge alert
  - `POST /api/v1/alerts/{id}/resolve` - Resolve alert

- **WebSocket**
  - `WS /api/v1/ws/stream/{camera_id}` - Live video stream
  - `WS /api/v1/ws/notifications` - Real-time notifications

## Configuration

### Environment Variables

#### Backend (.env)
```bash
# Application
SECRET_KEY=your-secret-key-here
DEBUG=False

# Database
POSTGRES_SERVER=postgres
POSTGRES_USER=saas_camera_user
POSTGRES_PASSWORD=your-password
POSTGRES_DB=saas_camera_db

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# AI Model
MODEL_PATH=./models/shoplifting_detection.pt
CONFIDENCE_THRESHOLD=0.5
```

#### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/api/v1/ws
```

## Camera Sources

The system supports multiple camera types:

1. **Webcam**: Use device index (e.g., "0" for default webcam)
2. **RTSP Stream**: Use RTSP URL (e.g., "rtsp://username:password@ip:port/stream")
3. **HTTP Stream**: Use HTTP URL (e.g., "http://ip:port/video")
4. **Video File**: Use file path (e.g., "/path/to/video.mp4")

## AI Model

The system uses YOLOv8 for object detection. By default, it uses YOLOv8n (nano) for fast inference.

### Custom Model

To use the shoplifting detection model from the reference repository:

1. Download the trained model
2. Place it in `backend/models/shoplifting_detection.pt`
3. Update `MODEL_PATH` in `.env`

### Training Your Own Model

You can train a custom YOLOv8 model for specific detection needs:

```python
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')

# Train the model
model.train(data='your-dataset.yaml', epochs=100)

# Export the model
model.export(format='pt')
```

## Deployment

### Production Deployment

1. **Update environment variables**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure production database

2. **Build production images**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up reverse proxy (nginx)**
   - Configure SSL/TLS certificates
   - Set up domain routing

4. **Database backups**
   ```bash
   docker exec ai_camera_postgres pg_dump -U saas_camera_user saas_camera_db > backup.sql
   ```

### Scaling

- Use load balancer for multiple backend instances
- Configure Redis for session storage
- Use object storage (S3) for video/image storage
- Set up monitoring (Prometheus/Grafana)

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Troubleshooting

### Webcam Access Issues

**Linux**: Add user to video group
```bash
sudo usermod -aG video $USER
```

**Docker**: Ensure device is mounted
```yaml
devices:
  - /dev/video0:/dev/video0
```

### Database Connection Issues

1. Check PostgreSQL is running: `docker ps`
2. Verify credentials in `.env`
3. Check database logs: `docker logs ai_camera_postgres`

### WebSocket Connection Issues

1. Ensure CORS settings allow WebSocket connections
2. Check firewall rules
3. Verify WebSocket URL in frontend `.env`

## Performance Optimization

1. **Model Optimization**
   - Use YOLOv8n for speed
   - Reduce input resolution
   - Adjust confidence threshold

2. **Video Processing**
   - Lower FPS for less CPU usage
   - Use GPU acceleration if available
   - Implement frame skipping

3. **Database**
   - Add indexes for frequent queries
   - Archive old detections
   - Use connection pooling

## Security

- All passwords are hashed with bcrypt
- JWT tokens for authentication
- CORS protection
- SQL injection protection via ORM
- Input validation with Pydantic
- Rate limiting (recommended for production)

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Documentation: [See /docs]

## Acknowledgments

- YOLOv8 by Ultralytics
- Reference shoplifting detection: https://github.com/alich03/Shoplifting-Detection-using-yolov8
- FastAPI framework
- React community

## Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Email notifications
- [ ] Advanced analytics
- [ ] Multi-tenant support
- [ ] Cloud deployment guides
- [ ] Kubernetes manifests
- [ ] CI/CD pipelines
- [ ] Performance monitoring
- [ ] Video recording and playback
- [ ] Face recognition integration

---

**Built with ❤️ for secure retail environments**
