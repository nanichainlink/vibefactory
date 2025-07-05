"""
Módulo para gestionar los clientes de API externos (Perplexity, Gemini, etc.).
"""
from typing import Optional, Dict, Any, Union
import os
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

# Importaciones condicionales para manejar dependencias opcionales
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Generative AI no está instalado. Instala con: pip install google-generativeai")

try:
    from langchain_community.llms import Perplexity
    PERPLEXITY_AVAILABLE = True
except ImportError:
    PERPLEXITY_AVAILABLE = False
    logger.warning("LangChain Community no está instalado. Instala con: pip install langchain-community")

class APIClients:
    """
    Clase para gestionar los clientes de API externos.
    
    Proporciona métodos para inicializar y acceder a los clientes de diferentes APIs de IA.
    """
    
    _instance = None
    _perplexity_client = None
    _gemini_client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIClients, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize_apis(cls, 
                       perplexity_api_key: Optional[str] = None, 
                       gemini_api_key: Optional[str] = None) -> None:
        """
        Inicializa los clientes de las APIs con las claves proporcionadas.
        
        Args:
            perplexity_api_key: Clave API de Perplexity
            gemini_api_key: Clave API de Google Gemini
        """
        # Inicializar cliente de Perplexity si se proporciona la clave
        if perplexity_api_key and PERPLEXITY_AVAILABLE:
            try:
                cls._perplexity_client = Perplexity(
                    temperature=0.7,
                    model="sonar-medium-online",
                    api_key=perplexity_api_key,
                    max_retries=3
                )
                logger.info("Cliente de Perplexity inicializado correctamente")
            except Exception as e:
                logger.error(f"Error al inicializar Perplexity: {e}")
                cls._perplexity_client = None
        
        # Inicializar cliente de Gemini si se proporciona la clave
        if gemini_api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=gemini_api_key)
                cls._gemini_client = genai.GenerativeModel('gemini-pro')
                logger.info("Cliente de Gemini inicializado correctamente")
            except Exception as e:
                logger.error(f"Error al inicializar Gemini: {e}")
                cls._gemini_client = None
    
    @property
    def perplexity(self) -> Optional[Any]:
        """
        Devuelve el cliente de Perplexity si está configurado.
        
        Returns:
            Optional[Any]: Instancia del cliente Perplexity o None si no está disponible
        """
        if not PERPLEXITY_AVAILABLE:
            logger.warning("Perplexity no está disponible. Instala langchain-community.")
            return None
        return self._perplexity_client
    
    @property
    def gemini(self) -> Optional[Any]:
        """
        Devuelve el cliente de Gemini si está configurado.
        
        Returns:
            Optional[Any]: Instancia del cliente Gemini o None si no está disponible
        """
        if not GEMINI_AVAILABLE:
            logger.warning("Gemini no está disponible. Instala google-generativeai.")
            return None
        return self._gemini_client
    
    def get_client_status(self) -> Dict[str, Union[bool, str]]:
        """
        Devuelve el estado de los clientes de API.
        
        Returns:
            Dict[str, Union[bool, str]]: Diccionario con el estado y mensaje de cada cliente
        """
        status = {}
        
        if not PERPLEXITY_AVAILABLE:
            status["perplexity"] = {"available": False, "message": "Paquete no instalado"}
        else:
            status["perplexity"] = {
                "available": self._perplexity_client is not None,
                "message": "Conectado" if self._perplexity_client else "No configurado"
            }
        
        if not GEMINI_AVAILABLE:
            status["gemini"] = {"available": False, "message": "Paquete no instalado"}
        else:
            status["gemini"] = {
                "available": self._gemini_client is not None,
                "message": "Conectado" if self._gemini_client else "No configurado"
            }
            
        return status

# Instancia global para importar
global_api_clients = APIClients()

def initialize_api_clients(perplexity_api_key: Optional[str] = None, 
                         gemini_api_key: Optional[str] = None) -> APIClients:
    """
    Inicializa los clientes de API y devuelve la instancia.
    
    Args:
        perplexity_api_key: Clave API de Perplexity
        gemini_api_key: Clave API de Google Gemini
        
    Returns:
        APIClients: Instancia de los clientes de API
    """
    try:
        global_api_clients.initialize_apis(perplexity_api_key, gemini_api_key)
        logger.info("Clientes de API inicializados correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar los clientes de API: {e}")
    
    return global_api_clients
