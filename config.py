"""
Configuración de la aplicación VibeFactory.

Este módulo maneja la configuración de la aplicación, incluyendo variables de entorno,
configuraciones por defecto y validaciones.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Configuración principal de la aplicación."""
    
    # Configuración de la aplicación
    APP_NAME: str = "VibeFactory"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Configuración de la API
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días
    
    # Configuración de la base de datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{BASE_DIR}/vibefactory.db"
    )
    
    # Configuración de la API de Perplexity
    PERPLEXITY_API_KEY: Optional[str] = os.getenv("PERPLEXITY_API_KEY")
    
    # Configuración de Streamlit
    STREAMLIT_THEME: dict = {
        "primaryColor": "#4e8ef9",
        "backgroundColor": "#f0f2f6",
        "secondaryBackgroundColor": "#ffffff",
        "textColor": "#262730",
        "font": "sans serif",
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @validator("PERPLEXITY_API_KEY", pre=True)
    def validate_perplexity_api_key(cls, v):
        """Valida que la API key de Perplexity esté configurada."""
        if not v:
            raise ValueError("PERPLEXITY_API_KEY no está configurada en las variables de entorno")
        return v


# Instancia de configuración global
settings = Settings()

# Crear directorios necesarios
os.makedirs(BASE_DIR / "static" / "css", exist_ok=True)
os.makedirs(BASE_DIR / "templates" / "email", exist_ok=True)
os.makedirs(BASE_DIR / "tests" / "unit", exist_ok=True)
os.makedirs(BASE_DIR / "tests" / "integration", exist_ok=True)
