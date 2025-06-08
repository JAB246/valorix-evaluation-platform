from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
import os
import logging
import logging.handlers
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Base
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Valorix Evaluation API"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    
    # External Services
    INSEE_API_KEY: Optional[str] = os.getenv("INSEE_API_KEY")
    BANQUE_FRANCE_API_KEY: Optional[str] = os.getenv("BANQUE_FRANCE_API_KEY")
    EUROSTAT_API_KEY: Optional[str] = os.getenv("EUROSTAT_API_KEY")
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Cache
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Sentry (monitoring et sécurité)
    SENTRY_DSN: str = ""
    
    # Environnement d'exécution
    ENVIRONMENT: str = "development"
    DEPLOYMENT_ENV: str = "development"
    FORCE_HTTPS: bool = False
    
    # Server settings
    SERVER_NAME: str = "valorix-api"
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Security headers
    SECURITY_HEADERS: Dict[str, str] = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
    }
    
    def configure_logging(self):
        """Configure le système de logging."""
        logging.basicConfig(
            level=getattr(logging, self.LOG_LEVEL.upper()),
            format=self.LOG_FORMAT,
            handlers=[
                logging.StreamHandler(),
                logging.handlers.RotatingFileHandler(
                    "valorix_api.log", 
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5
                )
            ]
        )
        
        # Logger spécifique pour l'API
        api_logger = logging.getLogger("valorix_api")
        api_logger.setLevel(getattr(logging, self.LOG_LEVEL.upper()))
        
        if self.ENVIRONMENT == "development":
            # Plus de détails en développement
            logging.getLogger("uvicorn").setLevel(logging.INFO)
            logging.getLogger("fastapi").setLevel(logging.DEBUG)
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Configuration des middlewares
MIDDLEWARE_CONFIG: Dict[str, Any] = {
    "trusted_hosts": ["*"],
    "allowed_hosts": settings.ALLOWED_HOSTS,
    "cors_origins": settings.BACKEND_CORS_ORIGINS,
    "cors_methods": settings.CORS_ALLOW_METHODS,
    "cors_headers": settings.CORS_ALLOW_HEADERS,
}

# Configuration de la base de données
DATABASE_CONFIG: Dict[str, Any] = {
    "url": settings.DATABASE_URL,
    "echo": False,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}

# Configuration du cache
CACHE_CONFIG: Dict[str, Any] = {
    "url": settings.REDIS_URL,
    "ttl": settings.CACHE_TTL,
    "prefix": "valorix:",
}

# Configuration des services externes
EXTERNAL_SERVICES_CONFIG: Dict[str, Any] = {
    "insee": {
        "api_key": settings.INSEE_API_KEY,
        "base_url": "https://api.insee.fr",
    },
    "banque_france": {
        "api_key": settings.BANQUE_FRANCE_API_KEY,
        "base_url": "https://api.banque-france.fr",
    },
    "eurostat": {
        "api_key": settings.EUROSTAT_API_KEY,
        "base_url": "https://ec.europa.eu/eurostat/api",
    },
} 
