import os
import re
import time
import socket
import httpx
from typing import Optional, List, Dict, Any, Generator, Union
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from pathlib import Path

class OllamaConnectionError(Exception):
    """Custom exception for Ollama connection issues"""
    pass

def check_ollama_connection(timeout: float = 5.0) -> bool:
    """Check if Ollama server is running and accessible"""
    try:
        # Try to connect to Ollama's default port (11434)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect(('localhost', 11434))
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def retry_on_connection_error(max_retries: int = 3, initial_delay: float = 1.0):
    """Decorator to retry a function on connection errors"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    if not check_ollama_connection():
                        raise OllamaConnectionError("Ollama server is not running or not accessible")
                    return func(*args, **kwargs)
                except (httpx.ReadError, httpx.ConnectError, httpx.ConnectTimeout, 
                       socket.timeout, ConnectionRefusedError, OSError) as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        delay = initial_delay * (2 ** attempt)  # Exponential backoff
                        time.sleep(delay)
                        continue
                    raise OllamaConnectionError(
                        f"Failed to connect to Ollama after {max_retries} attempts. "
                        f"Please ensure Ollama is running. Error: {str(e)}"
                    ) from e
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        delay = initial_delay * (2 ** attempt)
                        time.sleep(delay)
                        continue
                    raise
            raise last_error
        return wrapper
    return decorator
# agents.py

class PlannerAgent:
    """
    Agente encargado de descomponer los requisitos del proyecto en tareas.
    """
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.model = OllamaLLM(
            model=model_name,
            temperature=0.2,
            timeout=300,  # Increase timeout to 5 minutes
            num_predict=4096  # Limit response length if needed
        )
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Eres un 'Planificador de Proyectos IA' experto. Tu misión es descomponer la descripción de un proyecto de software en una lista de tareas numeradas, claras y concisas. Cada tarea debe ser un paso lógico para construir un MVP (Producto Mínimo Viable)."),
            ("user", "Descripción del proyecto: {description}\n\nPor favor, genera la lista de tareas.")
        ])
        self.chain = self.prompt_template | self.model | StrOutputParser()

    @retry_on_connection_error(max_retries=3, initial_delay=1.0)
    def _invoke_with_retry(self, input_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None, 
                          max_retries: int = 3, initial_delay: float = 1.0) -> Optional[str]:
        """
        Helper method to invoke the chain with retry logic.
        
        Args:
            input_data: The input data for the chain
            config: Optional configuration for the chain
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay between retries in seconds
            
        Returns:
            The result of the chain invocation or None if all attempts fail
            
        Raises:
            OllamaConnectionError: If connection to Ollama fails after all retries
            Exception: For other types of errors after all retries
        """
        last_error = None
        for attempt in range(max_retries):
            try:
                if not check_ollama_connection():
                    raise OllamaConnectionError("Ollama server is not running or not accessible")
                    
                if config:
                    return self.chain.invoke(input_data, config=config)
                return self.chain.invoke(input_data)
                
            except (httpx.ReadError, httpx.ConnectError, httpx.ConnectTimeout, 
                   socket.timeout, ConnectionRefusedError, OSError) as e:
                last_error = OllamaConnectionError(
                    f"Connection to Ollama failed (attempt {attempt + 1}/{max_retries}): {str(e)}"
                )
                if attempt < max_retries - 1:
                    delay = initial_delay * (2 ** attempt)
                    time.sleep(delay)
                continue
                
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    delay = initial_delay * (2 ** attempt)
                    time.sleep(delay)
                continue
        
        # If we get here, all retries failed
        error_msg = f"All {max_retries} attempts failed."
        if last_error:
            error_msg += f" Last error: {str(last_error)}"
        raise last_error if last_error else Exception("Unknown error occurred")

    def generate_tasks(self, description: str, callbacks=None) -> List[str]:
        """
        Genera una lista de tareas a partir de la descripción del proyecto.
        
        Args:
            description: Descripción del proyecto
            callbacks: Callbacks opcionales para el seguimiento
            
        Returns:
            Lista de tareas generadas o lista por defecto en caso de error
        """
        try:
            print(f"Generating tasks for description: {description[:100]}...")  # Debug
            
            # Validar la entrada
            if not description or not description.strip():
                print("Error: Empty project description")
                return self._get_default_tasks()
                
            # Verificar conexión con Ollama
            if not check_ollama_connection():
                print("Error: Ollama server is not running or not accessible")
                return self._get_default_tasks()
                
            try:
                # Llamar al modelo con manejo de errores mejorado
                response = self._invoke_with_retry({"description": description})
                
                # Si no hay respuesta después de los reintentos
                if not response:
                    print("Warning: No response from model after retries")
                    return self._get_default_tasks()
                    
                print(f"Raw response from model: {response[:200]}...")  # Debug
                
                # Procesar la respuesta para extraer las tareas
                tasks = self._parse_tasks(response)
                
                # Validar las tareas generadas
                if not tasks or len(tasks) < 2:
                    print("Warning: Insufficient number of tasks generated")
                    return self._get_default_tasks()
                    
                print(f"Successfully parsed {len(tasks)} tasks")  # Debug
                return tasks
                
            except OllamaConnectionError as e:
                print(f"Ollama connection error: {str(e)}")
                return self._get_default_tasks()
                
        except Exception as e:
            error_msg = f"Error en el Agente Planificador: {str(e)}"
            print(error_msg)
            # Return default tasks in case of error to keep the app running
            return self._get_default_tasks()
            
    def _parse_tasks(self, response: str) -> List[str]:
        """
        Parse the model response to extract a list of tasks.
        
        Args:
            response: Raw response from the model
            
        Returns:
            List of parsed and cleaned tasks
        """
        if not response or not isinstance(response, str):
            return self._get_default_tasks()
            
        # Try to find numbered tasks first (1., 2., etc.)
        tasks = [task.strip() for task in re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|$)', response, re.DOTALL)]
        
        # If no numbered tasks found, try to split by newlines
        if not tasks:
            tasks = [line.strip() for line in response.split('\n') if line.strip()]
        
        # Filter out empty tasks and ensure each task is a string
        tasks = [str(task).strip() for task in tasks if str(task).strip()]
        
        # If we still have no tasks, return a default set
        if not tasks:
            return self._get_default_tasks()
            
        return tasks
        
    def _get_default_tasks(self) -> List[str]:
        """
        Returns a default list of tasks to use when generation fails.
        
        Returns:
            List of default tasks
        """
        return [
            "1. Crear un archivo README.md con la descripción del proyecto",
            "2. Implementar la funcionalidad principal",
            "3. Añadir documentación básica",
            "4. Configurar el entorno de desarrollo",
            "5. Implementar pruebas unitarias"
        ]

class CodeGeneratorAgent:
    """
    Agente que genera fragmentos de código para cada tarea específica.
    """
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.model = OllamaLLM(
            model=model_name,
            temperature=0.3,
            timeout=300,  # Increase timeout to 5 minutes
            num_predict=4096  # Limit response length if needed
        )
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Eres un 'Generador de Código y Documentación IA' experto. Tu objetivo es escribir contenido relevante para una tarea específica. Si la tarea es de codificación, escribe código Python funcional y de alta calidad. Si la tarea es sobre diseño, planificación o documentación (como un GDD), escribe la respuesta en formato Markdown. El código debe estar en bloques ```python ... ``` y la documentación en bloques ```markdown ... ```. Siempre precede el bloque con el nombre del archivo (ej: '### app.py' o '### GDD.md')."),
            ("user", "Contexto del proyecto: {project_context}\n\nTarea actual: {task}\n\nGenera el contenido necesario para completar esta tarea. Si la tarea implica crear varios archivos, sepáralos con '### nombre_archivo.py' o '### nombre_archivo.md'.")
        ])
        self.chain = self.prompt_template | self.model | StrOutputParser()

    def stream_code(self, task: str, project_context: str, callbacks=None):
        """
        Genera un stream de fragmentos de código para una tarea.
        """
        return self.chain.stream(
            {"task": task, "project_context": project_context},
            config={"callbacks": callbacks} if callbacks else None
        )

    def sanitize_filename(self, filename: str, default: str = "app.py") -> str:
        """
        Sanitize and validate a filename.
        
        Args:
            filename: The original filename to sanitize
            default: Default filename to use if sanitization fails
            
        Returns:
            A sanitized filename with valid characters
        """
        if not filename or not isinstance(filename, str):
            return default
            
        # Remove any path components and keep only the filename
        filename = os.path.basename(filename)
        
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)
        
        # Ensure it has a valid extension
        if not re.search(r'\.(py|md|txt|json|yaml|yml|html|css|js)$', filename, re.IGNORECASE):
            # If no valid extension, add .py by default
            filename = f"{filename}.py"
            
        return filename.strip() or default

    def parse_code(self, response: str) -> dict[str, str]:
        """
        Parse the model response to extract filenames and their corresponding code/markdown blocks.
        
        Args:
            response: Raw response from the model
            
        Returns:
            Dictionary mapping filenames to their content
        """
        snippets = {}
        
        # First, try to find all code blocks with filenames
        pattern = r'###\s*(.*?)\s*```(?:python|markdown|)\n(.*?)\n```'
        matches = re.findall(pattern, response, re.DOTALL)
        
        if matches:
            for file_name, code in matches:
                if not file_name.strip():
                    continue
                    
                # Sanitize the filename
                sanitized_name = self.sanitize_filename(file_name)
                
                # Only add if we don't already have this filename
                if sanitized_name not in snippets:
                    snippets[sanitized_name] = code.strip()
        
        # Fallback: Look for any code blocks without filenames
        if not snippets:
            code_blocks = re.findall(r'```(?:python|markdown|)\n(.*?)\n```', response, re.DOTALL)
            for i, code in enumerate(code_blocks, 1):
                filename = f"app_{i}.py" if 'def ' in code or 'import ' in code else f"documentation_{i}.md"
                snippets[filename] = code.strip()
        
        return snippets

    def _detect_required_dependencies(self, code: str) -> list[str]:
        """
        Detecta dependencias comunes basadas en el código generado.
        
        Args:
            code: Código fuente a analizar
            
        Returns:
            Lista de dependencias requeridas
        """
        dependencies = []
        
        # Detectar frameworks web
        if any(imp in code for imp in ['from flask import', 'import flask', 'Flask(']):
            dependencies.append('flask')
        if any(imp in code for imp in ['from fastapi import', 'import fastapi', 'FastAPI(']):
            dependencies.append('fastapi')
            dependencies.append('uvicorn')
        
        # Detectar ORMs
        if any(imp in code for imp in ['from sqlalchemy import', 'import sqlalchemy']):
            dependencies.append('sqlalchemy')
        if any(imp in code for imp in ['from pymongo import', 'import pymongo']):
            dependencies.append('pymongo')
            
        # Detectar utilidades comunes
        if any(imp in code for imp in ['import pandas', 'from pandas import']):
            dependencies.append('pandas')
        if any(imp in code for imp in ['import numpy', 'from numpy import']):
            dependencies.append('numpy')
            
        return sorted(list(set(dependencies)))

    def generate_code(self, task: str, project_context: str, callbacks=None) -> dict[str, str]:
        """
        Genera un diccionario de archivos y su contenido de código para una tarea.
        
        Args:
            task: Tarea a implementar
            project_context: Contexto del proyecto
            callbacks: Callbacks opcionales para seguimiento
            
        Returns:
            Diccionario con nombres de archivo como clave y contenido como valor
        """
        try:
            # Generar el código principal
            response = self._invoke_with_retry(
                input_data={"task": task, "project_context": project_context},
                config={"callbacks": callbacks} if callbacks else None
            )
            
            # Parsear el código generado
            files = self.parse_code(response)
            
            # Si hay archivos Python, analizar dependencias
            python_files = {k: v for k, v in files.items() if k.endswith('.py')}
            if python_files:
                all_code = '\n'.join(python_files.values())
                dependencies = self._detect_required_dependencies(all_code)
                
                if dependencies:
                    files['requirements.txt'] = '\n'.join(dependencies) + '\n'
            return files
            
        except Exception as e:
            print(f"Error en el Agente Generador de Código: {e}")
            return {}
