"""
Módulo principal de la API de VibeFactory.

Proporciona los endpoints principales para la interacción con la aplicación.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
import uuid
from datetime import datetime

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VibeFactory API",
    description="API para la orquestación de agentes IA de VibeFactory",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class ProjectRequest(BaseModel):
    """Modelo para la creación de un nuevo proyecto."""
    description: str
    project_type: str = "web"
    config: Optional[Dict] = None

class TaskModel(BaseModel):
    """Modelo para representar una tarea."""
    id: int
    description: str
    status: str
    code: Optional[str] = None
    dependencies: List[int] = []

class ProjectResponse(BaseModel):
    """Modelo para la respuesta de un proyecto."""
    project_id: str
    status: str
    tasks: List[TaskModel]
    created_at: datetime
    updated_at: datetime

# Estado de la aplicación (en producción usar una base de datos)
projects_db = {}

@app.get("/")
async def root():
    """Endpoint raíz que devuelve información básica de la API."""
    return {
        "name": "VibeFactory API",
        "version": "0.1.0",
        "status": "running",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de estado."""
    return {"status": "healthy"}

@app.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectRequest):
    """
    Crea un nuevo proyecto y genera las tareas iniciales.
    
    Args:
        project: Datos del proyecto a crear
        
    Returns:
        Proyecto creado con las tareas generadas
    """
    try:
        project_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        # Crear tareas de ejemplo (en producción esto vendría del Planificador)
        tasks = [
            {
                "id": 1,
                "description": "Configuración inicial del proyecto",
                "status": "pending",
                "dependencies": []
            },
            {
                "id": 2,
                "description": "Implementar funcionalidad principal",
                "status": "pending",
                "dependencies": [1]
            },
            {
                "id": 3,
                "description": "Añadir pruebas unitarias",
                "status": "pending",
                "dependencies": [2]
            }
        ]
        
        # Crear proyecto
        project_data = {
            "project_id": project_id,
            "description": project.description,
            "project_type": project.project_type,
            "status": "initializing",
            "tasks": tasks,
            "created_at": timestamp,
            "updated_at": timestamp,
            "config": project.config or {}
        }
        
        # Guardar en la base de datos
        projects_db[project_id] = project_data
        
        # Crear respuesta
        response = ProjectResponse(**{
            "project_id": project_id,
            "status": project_data["status"],
            "tasks": [TaskModel(**task) for task in tasks],
            "created_at": timestamp,
            "updated_at": timestamp
        })
        
        logger.info(f"Proyecto creado: {project_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error al crear proyecto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear proyecto: {str(e)}"
        )

@app.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    Obtiene el estado actual de un proyecto.
    
    Args:
        project_id: ID del proyecto a consultar
        
    Returns:
        Estado actual del proyecto con sus tareas
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto {project_id} no encontrado"
        )
    
    project = projects_db[project_id]
    return ProjectResponse(**{
        "project_id": project_id,
        "status": project["status"],
        "tasks": [TaskModel(**task) for task in project["tasks"]],
        "created_at": project["created_at"],
        "updated_at": project["updated_at"]
    })

@app.post("/projects/{project_id}/tasks/{task_id}/generate")
async def generate_task_code(project_id: str, task_id: int):
    """
    Genera el código para una tarea específica.
    
    Args:
        project_id: ID del proyecto
        task_id: ID de la tarea a generar
        
    Returns:
        Resultado de la generación de código
    """
    if project_id not in projects_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto {project_id} no encontrado"
        )
    
    project = projects_db[project_id]
    task = next((t for t in project["tasks"] if t["id"] == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea {task_id} no encontrada en el proyecto {project_id}"
        )
    
    try:
        # Aquí iría la lógica para generar el código usando el Generador de Código
        # Por ahora, usamos código de ejemplo
        generated_code = f"# Código generado para la tarea {task_id}\n"
        generated_code += f"# {task['description']}\n\n"
        generated_code += "def main():\n    print('¡Hola desde VibeFactory!')\n\n"
        generated_code += "if __name__ == '__main__':\n    main()"
        
        # Actualizar la tarea con el código generado
        task["code"] = generated_code
        task["status"] = "completed"
        project["updated_at"] = datetime.utcnow()
        
        # Verificar si todas las tareas están completas
        if all(t["status"] == "completed" for t in project["tasks"]):
            project["status"] = "completed"
        
        return {
            "status": "success", 
            "task_id": task_id, 
            "code": generated_code,
            "project_status": project["status"]
        }
        
    except Exception as e:
        logger.error(f"Error al generar código para la tarea {task_id}: {str(e)}")
        task["status"] = "failed"
        project["status"] = "error"
        project["updated_at"] = datetime.utcnow()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar código: {str(e)}"
        )

# Ejemplo de uso:
# uvicorn vibefactory.api.main:app --reload
