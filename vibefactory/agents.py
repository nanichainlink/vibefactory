"""
Módulo de agentes IA para VibeFactory.

Contiene las implementaciones de los agentes Planificador y Generador de Código.
"""

import json
import logging
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
import httpx
import asyncio

# Importar utilidades locales
from .prompts import get_planner_prompt, get_coder_prompt

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30.0  # segundos

class Task(BaseModel):
    """Modelo para representar una tarea generada por el Planificador."""
    id: int
    description: str
    status: str = "pending"
    code: Optional[str] = None
    dependencies: List[int] = Field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la tarea a un diccionario."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "code": self.code,
            "dependencies": self.dependencies
        }

class BaseAgent:
    """Clase base para los agentes de IA."""
    
    def __init__(self, api_key: str, model: str = "llama-3-sonar-large-32k-online"):
        """
        Inicializa el agente con la configuración básica.
        
        Args:
            api_key: Clave de API para el servicio de IA
            model: Nombre del modelo a utilizar
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Realiza una solicitud a la API de Perplexity.
        
        Args:
            messages: Lista de mensajes para la conversación
            
        Returns:
            Respuesta de la API
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            for attempt in range(MAX_RETRIES):
                try:
                    response = await client.post(
                        url,
                        headers=self.headers,
                        json=payload
                    )
                    response.raise_for_status()
                    return response.json()
                except (httpx.HTTPError, json.JSONDecodeError) as e:
                    if attempt == MAX_RETRIES - 1:
                        logger.error(f"Error en la solicitud después de {MAX_RETRIES} intentos: {str(e)}")
                        raise
                    await asyncio.sleep(1 * (attempt + 1))  # Backoff exponencial
    
    def _extract_json_from_response(self, text: str) -> Union[Dict, List]:
        """
        Extrae un objeto JSON del texto de respuesta.
        
        Args:
            text: Texto de respuesta que puede contener JSON
            
        Returns:
            Objeto JSON extraído
        """
        try:
            # Buscar el primer { o [
            start = min(
                text.find('{') if '{' in text else float('inf'),
                text.find('[') if '[' in text else float('inf')
            )
            
            if start == float('inf'):
                raise ValueError("No se encontró un objeto JSON en la respuesta")
                
            # Buscar el cierre correspondiente
            stack = []
            end = -1
            
            for i in range(start, len(text)):
                char = text[i]
                if char in '{[':
                    stack.append(char)
                elif char in '}]':
                    if not stack:
                        break
                    stack.pop()
                    if not stack:
                        end = i + 1
                        break
            
            if end == -1:
                raise ValueError("No se pudo encontrar el cierre del objeto JSON")
                
            json_str = text[start:end].strip()
            return json.loads(json_str)
            
        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"Error al extraer JSON: {str(e)}")
            raise ValueError(f"No se pudo procesar la respuesta del modelo: {str(e)}")


class Planificador(BaseAgent):
    """
    Agente responsable de descomponer los requisitos del proyecto en tareas.
    """
    
    async def generate_tasks(self, project_description: str) -> List[Dict]:
        """
        Genera una lista de tareas a partir de la descripción del proyecto.
        
        Args:
            project_description: Descripción del proyecto
            
        Returns:
            Lista de diccionarios con la información de las tareas
        """
        messages = [
            {"role": "system", "content": get_planner_prompt(project_description)},
            {"role": "user", "content": project_description}
        ]
        
        try:
            response = await self._make_request(messages)
            content = response['choices'][0]['message']['content']
            
            # Extraer y validar el JSON de la respuesta
            tasks_data = self._extract_json_from_response(content)
            
            # Validar la estructura de las tareas
            if not isinstance(tasks_data, dict) or "tasks" not in tasks_data:
                raise ValueError("Formato de respuesta inválido: se esperaba un objeto con clave 'tasks'")
                
            return tasks_data["tasks"]
            
        except Exception as e:
            logger.error(f"Error al generar tareas: {str(e)}")
            raise


class GeneradorCodigo(BaseAgent):
    """
    Agente responsable de generar código para tareas específicas.
    """
    
    async def generate_code(self, task: Dict, project_context: Dict) -> Dict:
        """
        Genera código para una tarea específica.
        
        Args:
            task: Diccionario con la información de la tarea
            project_context: Contexto del proyecto
            
        Returns:
            Diccionario con el código generado y metadatos
        """
        prompt = get_coder_prompt(task, project_context)
        
        messages = [
            {"role": "system", "content": "Eres un asistente de programación experto en Python, Streamlit y FastAPI."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self._make_request(messages)
            content = response['choices'][0]['message']['content']
            
            # Extraer y validar el JSON de la respuesta
            result = self._extract_json_from_response(content)
            
            # Validar la estructura de la respuesta
            if not isinstance(result, dict) or "files" not in result:
                raise ValueError("Formato de respuesta inválido: se esperaba un objeto con clave 'files'")
                
            return result
            
        except Exception as e:
            logger.error(f"Error al generar código para tarea {task.get('id')}: {str(e)}")
            return {
                "task_id": task.get('id'),
                "files": [{
                    "path": "error.py",
                    "code": f"# Error al generar código: {str(e)}",
                    "description": "Error en la generación de código"
                }],
                "dependencies": [],
                "instructions": "No se pudo generar el código. Por favor, revisa los logs para más detalles."
            }
