"""
Utilidades y funciones de ayuda para VibeFactory.

Incluye manejo de contexto, configuración y utilidades generales.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProjectContext:
    """Clase para manejar el contexto del proyecto generado."""
    
    def __init__(self, project_name: str, description: str, base_path: str = "./projects"):
        """
        Inicializa un nuevo contexto de proyecto.
        
        Args:
            project_name: Nombre del proyecto
            description: Descripción del proyecto
            base_path: Ruta base donde se guardarán los proyectos
        """
        self.project_name = self._sanitize_name(project_name)
        self.description = description
        self.base_path = Path(base_path) / self.project_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.metadata = {
            "name": self.project_name,
            "description": description,
            "created_at": self.timestamp,
            "status": "initializing",
            "tasks": []
        }
        self._setup_project_structure()
    
    def _sanitize_name(self, name: str) -> str:
        """Limpia y formatea el nombre del proyecto."""
        # Reemplazar caracteres no permitidos
        name = "".join(c if c.isalnum() or c in "-_ " else "_" for c in name)
        # Reemplazar espacios con guiones bajos
        return name.replace(" ", "_")
    
    def _setup_project_structure(self):
        """Crea la estructura de directorios del proyecto."""
        try:
            # Directorio raíz del proyecto
            self.base_path.mkdir(parents=True, exist_ok=True)
            
            # Subdirectorios comunes
            (self.base_path / "src").mkdir(exist_ok=True)
            (self.base_path / "tests").mkdir(exist_ok=True)
            (self.base_path / "docs").mkdir(exist_ok=True)
            (self.base_path / "config").mkdir(exist_ok=True)
            
            # Archivo de metadatos
            self._save_metadata()
            
            logger.info(f"Estructura del proyecto creada en: {self.base_path}")
            
        except Exception as e:
            logger.error(f"Error al crear la estructura del proyecto: {str(e)}")
            raise
    
    def _save_metadata(self):
        """Guarda los metadatos del proyecto en un archivo."""
        try:
            with open(self.base_path / "project_metadata.json", "w") as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error al guardar metadatos: {str(e)}")
    
    def add_task_result(self, task_id: int, task_description: str, generated_code: str, status: str = "completed"):
        """
        Registra el resultado de una tarea en los metadatos del proyecto.
        
        Args:
            task_id: ID de la tarea
            task_description: Descripción de la tarea
            generated_code: Código generado para la tarea
            status: Estado de la tarea (pending, in_progress, completed, failed)
        """
        self.metadata["tasks"].append({
            "id": task_id,
            "description": task_description,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "code_length": len(generated_code) if generated_code else 0
        })
        self._save_metadata()
    
    def save_code_file(self, file_path: str, content: str):
        """
        Guarda un archivo de código en el proyecto.
        
        Args:
            file_path: Ruta relativa al directorio del proyecto
            content: Contenido del archivo
        """
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            logger.info(f"Archivo guardado: {full_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al guardar archivo {file_path}: {str(e)}")
            return False

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Carga la configuración desde un archivo YAML.
    
    Args:
        config_path: Ruta al archivo de configuración
        
    Returns:
        Diccionario con la configuración cargada
    """
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning(f"Archivo de configuración no encontrado: {config_path}")
        return {}
    except Exception as e:
        logger.error(f"Error al cargar configuración: {str(e)}")
        return {}

def save_config(config: Dict[str, Any], config_path: str = "config/config.yaml"):
    """
    Guarda la configuración en un archivo YAML.
    
    Args:
        config: Diccionario con la configuración
        config_path: Ruta donde guardar el archivo
    """
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
    except Exception as e:
        logger.error(f"Error al guardar configuración: {str(e)}")

def get_default_project_structure(project_type: str) -> Dict[str, Any]:
    """
    Devuelve una estructura de proyecto predeterminada según el tipo.
    
    Args:
        project_type: Tipo de proyecto (web, cli, api, etc.)
        
    Returns:
        Estructura del proyecto como diccionario
    """
    structures = {
        "web": {
            "src/": {
                "templates/": {},
                "static/": {
                    "css/": {},
                    "js/": {},
                    "images/": {}
                },
                "__init__.py": "",
                "app.py": ""
            },
            "tests/": {},
            "requirements.txt": "",
            "README.md": ""
        },
        "api": {
            "src/": {
                "api/": {
                    "__init__.py": "",
                    "endpoints/": {},
                    "models/": {},
                    "schemas/": {}
                },
                "__init__.py": "",
                "main.py": ""
            },
            "tests/": {},
            "requirements.txt": "",
            "README.md": ""
        }
    }
    
    return structures.get(project_type.lower(), {})

def zip_project(project_path: str, output_path: Optional[str] = None) -> Optional[str]:
    """
    Comprime un proyecto en un archivo ZIP.
    
    Args:
        project_path: Ruta al directorio del proyecto
        output_path: Ruta de salida para el archivo ZIP (opcional)
        
    Returns:
        Ruta al archivo ZIP generado o None en caso de error
    """
    import zipfile
    from pathlib import Path
    
    try:
        project_path = Path(project_path).resolve()
        if not output_path:
            output_path = f"{project_path.name}.zip"
            
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(project_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.relpath(file_path, project_path.parent)
                    zipf.write(file_path, arcname)
        
        return str(Path(output_path).resolve())
    except Exception as e:
        logger.error(f"Error al comprimir el proyecto: {str(e)}")
        return None
