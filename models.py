"""
Modelos de datos principales para VibeFactory.

Este módulo define los modelos Pydantic que se utilizan en toda la aplicación
para la validación y documentación de datos.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


class ProjectStatus(str, Enum):
    """Estados posibles de un proyecto."""
    DRAFT = "draft"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(str, Enum):
    """Estados posibles de una tarea."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectBase(BaseModel):
    """Modelo base para proyectos."""
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del proyecto")
    description: str = Field(..., min_length=10, description="Descripción detallada del proyecto")
    requirements: List[str] = Field(
        default_factory=list, 
        description="Lista de requisitos o características del proyecto"
    )
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT, description="Estado actual del proyecto")
    tags: List[str] = Field(
        default_factory=list, 
        description="Etiquetas para categorizar el proyecto"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadatos adicionales del proyecto"
    )


class ProjectCreate(ProjectBase):
    """Modelo para la creación de un nuevo proyecto."""
    pass


class ProjectUpdate(BaseModel):
    """Modelo para actualizar un proyecto existente."""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    status: Optional[ProjectStatus] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class Project(ProjectBase):
    """Modelo completo de proyecto con campos generados por el sistema."""
    id: str = Field(..., description="Identificador único del proyecto")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(..., description="ID del usuario que creó el proyecto")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TaskBase(BaseModel):
    """Modelo base para tareas."""
    title: str = Field(..., min_length=3, max_length=200, description="Título de la tarea")
    description: str = Field(..., description="Descripción detallada de la tarea")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Estado actual de la tarea")
    depends_on: List[str] = Field(
        default_factory=list,
        description="Lista de IDs de tareas de las que depende esta tarea"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadatos adicionales de la tarea"
    )


class TaskCreate(TaskBase):
    """Modelo para la creación de una nueva tarea."""
    project_id: str = Field(..., description="ID del proyecto al que pertenece la tarea")


class TaskUpdate(BaseModel):
    """Modelo para actualizar una tarea existente."""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    depends_on: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class Task(TaskBase):
    """Modelo completo de tarea con campos generados por el sistema."""
    id: str = Field(..., description="Identificador único de la tarea")
    project_id: str = Field(..., description="ID del proyecto al que pertenece la tarea")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CodeArtifact(BaseModel):
    """Modelo para artefactos de código generados por el sistema."""
    id: str = Field(..., description="Identificador único del artefacto")
    task_id: str = Field(..., description="ID de la tarea asociada")
    project_id: str = Field(..., description="ID del proyecto asociado")
    file_path: str = Field(..., description="Ruta relativa del archivo generado")
    content: str = Field(..., description="Contenido del archivo generado")
    language: str = Field(..., description="Lenguaje de programación")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
