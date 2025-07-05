"""
Servicio de orquestación para VibeFactory.

Coordina la interacción entre los agentes IA y gestiona el flujo de trabajo.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from ..agents import Planificador, GeneradorCodigo
from ..utils import ProjectContext

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Coordina la interacción entre los agentes IA y gestiona el flujo de trabajo.
    """
    
    def __init__(self, perplexity_api_key: str):
        """
        Inicializa el orquestador con los agentes necesarios.
        
        Args:
            perplexity_api_key: Clave de API para Perplexity
        """
        self.planificador = Planificador(api_key=perplexity_api_key)
        self.generador_codigo = GeneradorCodigo(api_key=perplexity_api_key)
        self.active_projects: Dict[str, Dict] = {}
        self.metrics = {
            "total_projects": 0,
            "active_projects": 0,
            "completed_projects": 0,
            "failed_projects": 0,
            "avg_generation_time": 0.0,
            "success_rate": 1.0
        }
    
    def create_project(self, description: str, project_type: str = "web") -> Dict[str, Any]:
        """
        Crea un nuevo proyecto y genera las tareas iniciales.
        
        Args:
            description: Descripción del proyecto
            project_type: Tipo de proyecto (web, api, etc.)
            
        Returns:
            Diccionario con los datos del proyecto creado
        """
        project_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        try:
            # Generar tareas con el Planificador
            tasks_data = self.planificador.generate_tasks(description)
            
            # Crear contexto del proyecto
            project_context = ProjectContext(
                project_name=f"project_{project_id[:8]}",
                description=description
            )
            
            # Crear estructura del proyecto
            project_data = {
                "project_id": project_id,
                "description": description,
                "project_type": project_type,
                "status": "initializing",
                "tasks": [
                    {
                        "id": task.id,
                        "description": task.description,
                        "status": "pending",
                        "dependencies": task.dependencies,
                        "code": None
                    }
                    for task in tasks_data
                ],
                "context": project_context,
                "created_at": timestamp,
                "updated_at": timestamp,
                "start_time": datetime.now().timestamp(),
                "metrics": {
                    "tasks_completed": 0,
                    "tasks_failed": 0,
                    "total_tasks": len(tasks_data)
                }
            }
            
            # Registrar proyecto
            self.active_projects[project_id] = project_data
            self.metrics["total_projects"] += 1
            self.metrics["active_projects"] += 1
            
            return project_data
            
        except Exception as e:
            logger.error(f"Error al crear proyecto: {str(e)}")
            self.metrics["failed_projects"] += 1
            self._update_success_rate()
            raise
    
    def generate_task_code(self, project_id: str, task_id: int) -> Dict[str, Any]:
        """
        Genera el código para una tarea específica.
        
        Args:
            project_id: ID del proyecto
            task_id: ID de la tarea
            
        Returns:
            Diccionario con el resultado de la generación
        """
        if project_id not in self.active_projects:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        project = self.active_projects[project_id]
        task = next((t for t in project["tasks"] if t["id"] == task_id), None)
        
        if not task:
            raise ValueError(f"Tarea {task_id} no encontrada en el proyecto {project_id}")
        
        # Verificar dependencias
        for dep_id in task.get("dependencies", []):
            dep_task = next((t for t in project["tasks"] if t["id"] == dep_id), None)
            if not dep_task or dep_task["status"] != "completed":
                raise ValueError(f"La tarea {task_id} tiene dependencias no cumplidas")
        
        try:
            # Generar código con el Generador de Código
            project_context = project["context"]
            code = self.generador_codigo.generate_code(
                task=task,
                project_context={
                    "technologies": ["Python", "Streamlit", "FastAPI"],
                    "structure": "Modular con separación clara de responsabilidades"
                }
            )
            
            # Actualizar estado de la tarea
            task["code"] = code
            task["status"] = "completed"
            project["updated_at"] = datetime.utcnow()
            project["metrics"]["tasks_completed"] += 1
            
            # Verificar si todas las tareas están completas
            if all(t["status"] == "completed" for t in project["tasks"]):
                project["status"] = "completed"
                project["end_time"] = datetime.now().timestamp()
                self.metrics["active_projects"] -= 1
                self.metrics["completed_projects"] += 1
                self._update_generation_time(project)
                
                # Generar archivo ZIP del proyecto
                self._generate_project_archive(project_id)
            
            return {
                "status": "success",
                "task_id": task_id,
                "code": code,
                "project_status": project["status"]
            }
            
        except Exception as e:
            logger.error(f"Error al generar código para la tarea {task_id}: {str(e)}")
            task["status"] = "failed"
            project["status"] = "error"
            project["metrics"]["tasks_failed"] += 1
            project["updated_at"] = datetime.utcnow()
            self.metrics["failed_projects"] += 1
            self._update_success_rate()
            
            raise
    
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """
        Obtiene los datos de un proyecto.
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Diccionario con los datos del proyecto
        """
        if project_id not in self.active_projects:
            raise ValueError(f"Proyecto {project_id} no encontrado")
        
        return self.active_projects[project_id]
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Obtiene las métricas actuales del sistema.
        
        Returns:
            Diccionario con las métricas
        """
        return self.metrics
    
    def _update_generation_time(self, project: Dict[str, Any]):
        """
        Actualiza el tiempo promedio de generación de proyectos.
        """
        if "start_time" in project and "end_time" in project:
            gen_time = project["end_time"] - project["start_time"]
            total_projects = self.metrics["completed_projects"] + self.metrics["failed_projects"]
            
            # Calcular nuevo promedio
            self.metrics["avg_generation_time"] = (
                (self.metrics["avg_generation_time"] * (total_projects - 1) + gen_time) 
                / total_projects
            )
    
    def _update_success_rate(self):
        """Actualiza la tasa de éxito de los proyectos."""
        total = self.metrics["completed_projects"] + self.metrics["failed_projects"]
        if total > 0:
            self.metrics["success_rate"] = self.metrics["completed_projects"] / total
    
    def _generate_project_archive(self, project_id: str) -> str:
        """
        Genera un archivo ZIP con el proyecto completo.
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Ruta al archivo ZIP generado
        """
        # Esta implementación es un esqueleto
        # En una implementación real, aquí se generaría el ZIP con todos los archivos
        logger.info(f"Generando archivo ZIP para el proyecto {project_id}")
        return f"/tmp/{project_id}.zip"
