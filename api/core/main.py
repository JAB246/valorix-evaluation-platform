import logging

import sentry_sdk
from core.config import settings
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

# Initialize Sentry
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            SqlalchemyIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        enable_tracing=True,
        trace_propagation_targets=settings.ALLOWED_HOSTS if hasattr(settings, 'ALLOWED_HOSTS') else ["*"],
        before_send=lambda event, hint: (
            {
                **event,
                "server_name": getattr(settings, 'SERVER_NAME', 'valorix-api'),
                "tags": {
                    **(event.get("tags", {})),
                    "app_version": settings.VERSION,
                    "deployment": getattr(settings, 'DEPLOYMENT_ENV', 'development'),
                },
            }
            if settings.ENVIRONMENT == "production"
            else None
        ),
        sample_rate=1.0 if settings.ENVIRONMENT != "production" else 0.1,
        release=settings.VERSION,
        send_default_pii=False,
        _experiments={
            "profiles_sample_rate": 1.0,
            "trace_propagation_targets": getattr(settings, 'ALLOWED_HOSTS', ["*"]),
        },
    )

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Force HTTPS in production
if settings.ENVIRONMENT == "production" and getattr(settings, 'FORCE_HTTPS', False):
    app.add_middleware(HTTPSRedirectMiddleware)

# Set up rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Set up CORS with production settings
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=getattr(settings, 'CORS_ALLOW_CREDENTIALS', True),
        allow_methods=getattr(settings, 'CORS_ALLOW_METHODS', ["*"]),
        allow_headers=getattr(settings, 'CORS_ALLOW_HEADERS', ["*"]),
        expose_headers=["*"],
        max_age=3600,
    )

# Global error handlers
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    if settings.SENTRY_DSN:
        with sentry_sdk.push_scope() as scope:
            scope.set_context(
                "request",
                {
                    "url": str(request.url),
                    "method": request.method,
                    "headers": dict(request.headers),
                },
            )
            sentry_sdk.capture_exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": (
                str(exc)
                if settings.ENVIRONMENT != "production"
                else "Internal server error"
            ),
        },
    )


# Routeurs de base - commentés pour éviter les erreurs d'import
# TODO: Décommenter et réparer les imports des routeurs individuels
"""
# Import des nouveaux routeurs centralisés
def _import_router(name):
    return __import__(f"core.routers.{name}", fromlist=["router"]).router

prediction_router = _import_router("prediction_router")
file_upload_router = _import_router("file_upload")
extraction_router = _import_router("extraction_router")
benchmark_router = _import_router("benchmark_router")
chat_router = _import_router("chat_router")
dashboar...