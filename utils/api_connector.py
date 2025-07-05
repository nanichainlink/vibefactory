"""
Módulo ligero para la conexión con APIs de IA (Perplexity, Gemini, etc.).

Este módulo proporciona una implementación ligera sin dependencias pesadas
que puedan causar conflictos de versiones.
"""
import os
import json
import logging
from typing import Dict, Optional, Any, Union
import httpx

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAPIClient:
    """Clase base para clientes de API."""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Inicializa el cliente de API.
        
        Args:
            api_key: Clave API para autenticación
            base_url: URL base de la API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/') if base_url else None
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def close(self):
        """Cierra la sesión del cliente HTTP."""
        await self.client.aclose()
    
    def is_configured(self) -> bool:
        """Verifica si el cliente está configurado correctamente."""
        return bool(self.api_key and self.base_url)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Devuelve el estado del cliente.
        
        Returns:
            Dict con información del estado
        """
        return {
            "configured": self.is_configured(),
            "api_key": "*" * 8 if self.api_key else None,
            "base_url": self.base_url
        }


class PerplexityClient(BaseAPIClient):
    """Cliente para la API de Perplexity AI."""
    
    def __init__(self, api_key: str = None):
        """
        Inicializa el cliente de Perplexity.
        
        Args:
            api_key: Clave API de Perplexity
        """
        super().__init__(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def query(self, prompt: str, model: str = "sonar-medium-online") -> Dict[str, Any]:
        """
        Envía una consulta a la API de Perplexity.
        
        Args:
            prompt: El prompt a enviar
            model: El modelo a utilizar
            
        Returns:
            Respuesta de la API
        """
        if not self.is_configured():
            raise ValueError("Cliente no configurado correctamente")
            
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = await self.client.post(
                url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en la consulta a Perplexity: {e}")
            raise


class GeminiClient(BaseAPIClient):
    """Cliente para la API de Google Gemini."""
    
    def __init__(self, api_key: str = None):
        """
        Inicializa el cliente de Gemini.
        
        Args:
            api_key: Clave API de Gemini
        """
        super().__init__(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta"
        )
    
    async def query(self, prompt: str, model: str = "gemini-pro") -> Dict[str, Any]:
        """
        Envía una consulta a la API de Gemini.
        
        Args:
            prompt: El prompt a enviar
            model: El modelo a utilizar
            
        Returns:
            Respuesta de la API
        """
        if not self.is_configured():
            raise ValueError("Cliente no configurado correctamente")
            
        url = f"{self.base_url}/models/{model}:generateContent"
        params = {"key": self.api_key}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            response = await self.client.post(
                url,
                params=params,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en la consulta a Gemini: {e}")
            raise


class APIConnector:
    """
    Clase para gestionar múltiples clientes de API.
    
    Proporciona una interfaz unificada para interactuar con diferentes APIs de IA.
    """
    
    def __init__(self):
        """Inicializa el conector de API."""
        self.clients = {
            "perplexity": None,
            "gemini": None
        }
    
    def configure_client(self, client_name: str, api_key: str) -> None:
        """
        Configura un cliente de API.
        
        Args:
            client_name: Nombre del cliente ('perplexity' o 'gemini')
            api_key: Clave API para el cliente
        """
        if not api_key:
            self.clients[client_name] = None
            return
            
        if client_name == "perplexity":
            self.clients[client_name] = PerplexityClient(api_key=api_key)
        elif client_name == "gemini":
            self.clients[client_name] = GeminiClient(api_key=api_key)
        else:
            raise ValueError(f"Cliente no soportado: {client_name}")
    
    def get_client(self, client_name: str) -> Optional[BaseAPIClient]:
        """
        Obtiene un cliente de API configurado.
        
        Args:
            client_name: Nombre del cliente ('perplexity' o 'gemini')
            
        Returns:
            Instancia del cliente o None si no está configurado
        """
        client = self.clients.get(client_name)
        return client if client and client.is_configured() else None
    
    def get_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtiene el estado de todos los clientes.
        
        Returns:
            Dict con el estado de cada cliente
        """
        status = {}
        for name, client in self.clients.items():
            if client is None:
                status[name] = {"configured": False, "status": "No configurado"}
            else:
                status[name] = {
                    "configured": client.is_configured(),
                    "status": "Conectado" if client.is_configured() else "Configuración incompleta"
                }
        return status
    
    async def close(self):
        """Cierra todas las conexiones de los clientes."""
        for client in self.clients.values():
            if client is not None:
                await client.close()


# Instancia global del conector de API
api_connector = APIConnector()

# Funciones de conveniencia
def configure_apis(perplexity_api_key: str = None, gemini_api_key: str = None) -> None:
    """
    Configura los clientes de API.
    
    Args:
        perplexity_api_key: Clave API de Perplexity
        gemini_api_key: Clave API de Gemini
    """
    if perplexity_api_key is not None:
        api_connector.configure_client("perplexity", perplexity_api_key)
    if gemini_api_key is not None:
        api_connector.configure_client("gemini", gemini_api_key)


def get_api_status() -> Dict[str, Dict[str, Any]]:
    """
    Obtiene el estado de las APIs configuradas.
    
    Returns:
        Dict con el estado de cada API
    """
    return api_connector.get_status()
