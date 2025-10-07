"""
Main FastAPI application entry point
Healthcare WhatsApp Bot API
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from typing import AsyncGenerator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple settings class (since we don't have your config module yet)
class SimpleSettings:
    APP_NAME: str = "Healthcare WhatsApp Bot"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SENTRY_DSN: str = ""
    WHATSAPP_WEBHOOK_URL: str = "/api/v1/webhook/whatsapp"
    MAX_FILE_SIZE: int = 16 * 1024 * 1024

settings = SimpleSettings()

# Simple database initialization functions
async def init_db():
    """Initialize database"""
    logger.info("🗄️ Initializing database...")
    # Add your database initialization code here
    pass

async def close_db():
    """Close database connections"""
    logger.info("🗄️ Closing database connections...")
    # Add your database cleanup code here
    pass

# Simple integrations initialization functions
async def initialize_integrations():
    """Initialize external integrations"""
    logger.info("🔌 Initializing integrations...")
    # Add your integration initialization code here
    pass

async def cleanup_integrations():
    """Cleanup external integrations"""
    logger.info("🔌 Closing integration connections...")
    # Add your integration cleanup code here
    pass

# Simple services initialization functions
async def initialize_services():
    """Initialize services"""
    logger.info("⚙️ Initializing services...")
    # Add your service initialization code here
    pass

async def cleanup_services():
    """Cleanup services"""
    logger.info("⚙️ Cleaning up services...")
    # Add your service cleanup code here
    pass

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("=" * 50)
    logger.info(f"🚀 Starting {settings.APP_NAME}")
    logger.info(f"📌 Version: {settings.API_VERSION}")
    logger.info(f"🔧 Debug Mode: {settings.DEBUG}")
    logger.info("=" * 50)
    
    try:
        # Initialize database
        logger.info("🗄️ Initializing database...")
        await init_db()
        logger.info("✅ Database initialized")
        
        # Initialize external integrations
        logger.info("🔌 Initializing integrations...")
        await initialize_integrations()
        logger.info("✅ Integrations initialized")
        
        # Initialize services
        logger.info("⚙️ Initializing services...")
        await initialize_services()
        logger.info("✅ Services initialized")
        
        logger.info("=" * 50)
        logger.info(f"✅ {settings.APP_NAME} is ready!")
        logger.info(f"📡 Webhook URL: {settings.WHATSAPP_WEBHOOK_URL}")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    logger.info("=" * 50)
    logger.info(f"🛑 Shutting down {settings.APP_NAME}")
    logger.info("=" * 50)
    
    try:
        # Cleanup services
        logger.info("🧹 Cleaning up services...")
        await cleanup_services()
        
        # Cleanup integrations
        logger.info("🔌 Closing integration connections...")
        await cleanup_integrations()
        
        # Close database
        logger.info("🗄️ Closing database connections...")
        await close_db()
        
        logger.info("✅ Shutdown complete")
        
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {str(e)}", exc_info=True)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Production-ready Healthcare WhatsApp Bot with AI-powered responses",
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes (we'll create simple ones)
@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.API_VERSION,
        "status": "running",
        "health_check": "/api/v1/health",
        "webhook": "/api/v1/webhook/whatsapp",
        "documentation": "/api/docs" if settings.DEBUG else None,
        "message": "Healthcare WhatsApp Bot API is running!"
    }

# Health check endpoints
@app.get("/api/v1/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "service": "Healthcare WhatsApp Bot",
        "version": settings.API_VERSION
    }

@app.get("/api/v1/health/db")
async def database_health():
    """
    Database connectivity health check
    """
    try:
        # Add your database check logic here
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@app.get("/api/v1/health/ready")
async def readiness_check():
    """
    Kubernetes readiness probe endpoint
    """
    return {
        "status": "ready",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/api/v1/health/live")
async def liveness_check():
    """
    Kubernetes liveness probe endpoint
    """
    return {
        "status": "alive",
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Webhook endpoints
@app.get("/api/v1/webhook/whatsapp")
async def whatsapp_webhook_verify():
    """
    WhatsApp webhook verification endpoint
    """
    logger.info("Webhook verification requested")
    return {
        "status": "ok",
        "message": "WhatsApp webhook active",
        "endpoint": "/api/v1/webhook/whatsapp"
    }

@app.post("/api/v1/webhook/whatsapp")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    To: str = Form(...),
    Body: str = Form(""),
    MessageSid: str = Form(...),
    NumMedia: int = Form(0),
):
    """
    Main WhatsApp webhook endpoint for receiving messages from Twilio
    """
    try:
        logger.info(f"📱 Received message from {From}: {Body[:100]}...")
        
        # Simple response for testing
        response_text = f"🏥 Healthcare Bot received: '{Body}'"
        
        if not Body:
            response_text = "🏥 Hello! I'm your Healthcare Assistant. How can I help you today?"
        
        # Create TwiML response
        from twilio.twiml.messaging_response import MessagingResponse
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(response_text)
        
        return PlainTextResponse(str(resp), media_type="text/xml")
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        # Return error response
        from twilio.twiml.messaging_response import MessagingResponse
        resp = MessagingResponse()
        msg = resp.message()
        msg.body("❌ Sorry, I encountered an error processing your message. Please try again.")
        return PlainTextResponse(str(resp), media_type="text/xml")

# Custom error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """
    Custom 404 error handler
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested endpoint {request.url.path} was not found",
            "path": request.url.path
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """
    Custom 500 error handler
    """
    logger.error(f"Internal server error: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

# Load balancer health check
@app.get("/health/lb")
async def load_balancer_health():
    """
    Simple health check for load balancers
    Returns 200 if service is up
    """
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    
    # Development server configuration
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
        log_level="debug" if settings.DEBUG else "info",
        access_log=settings.DEBUG,
    )