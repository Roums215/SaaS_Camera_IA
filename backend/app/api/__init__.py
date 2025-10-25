from fastapi import APIRouter
from app.api.endpoints import auth, cameras, detections, alerts, websocket

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(cameras.router, prefix="/cameras", tags=["Cameras"])
api_router.include_router(detections.router, prefix="/detections", tags=["Detections"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])
