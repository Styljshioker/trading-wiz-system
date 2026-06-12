from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.database import create_tables
from app.core.redis_client import redis_client
from app.services.trading_engine import TradingEngine
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global trading engine instance
trading_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🧙‍♂️ Starting Trading Wiz System...")
    
    # Create database tables
    await create_tables()
    logger.info("✅ Database tables created")
    
    # Initialize Redis connection
    await redis_client.ping()
    logger.info("✅ Redis connection established")
    
    # Initialize trading engine
    global trading_engine
    trading_engine = TradingEngine()
    await trading_engine.initialize()
    logger.info("✅ Trading engine initialized")
    
    logger.info("🚀 Trading Wiz System is ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Trading Wiz System...")
    if trading_engine:
        await trading_engine.shutdown()
    await redis_client.close()
    logger.info("✅ Shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="🧙‍♂️ Trading Wiz System API",
    description="Comprehensive AI-powered trading platform with intelligent bots, market analysis, and risk management",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "🧙‍♂️ Welcome to Trading Wiz System API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    try:
        # Check Redis connection
        await redis_client.ping()
        redis_status = "healthy"
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "services": {
            "api": "healthy",
            "redis": redis_status,
            "trading_engine": "healthy" if trading_engine else "not initialized"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
