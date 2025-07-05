import streamlit as st
import zipfile
import io
import os
import json
from langchain.callbacks.base import BaseCallbackHandler

class StreamlitCallbackHandler(BaseCallbackHandler):
    """
    Un manejador de callbacks que escribe los pensamientos y acciones de los agentes
    en un contenedor de Streamlit.
    """
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """
        Maneja la recepción de un nuevo token del LLM y lo añade al contenedor.
        """
        self.text += token
        self.container.info(self.text)

def save_project(project_name: str, files: dict[str, str]):
    """
    Guarda los archivos de un proyecto en un subdirectorio dedicado.
    
    Args:
        project_name: El nombre del subdirectorio del proyecto.
        files: Un diccionario de nombres de archivo y su contenido.
    """
    project_dir = os.path.join("projects", project_name)
    os.makedirs(project_dir, exist_ok=True)
    
    for file_name, content in files.items():
        file_path = os.path.join(project_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def download_project(files: dict[str, str], project_name: str):
    """
    Crea un botón de descarga en Streamlit para un proyecto generado.
    
    Args:
        files: Un diccionario donde las claves son nombres de archivo y los
               valores son el contenido del archivo.
        project_name: El nombre para el archivo zip.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, content in files.items():
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = content
            zip_file.writestr(file_name, content_bytes)

    st.download_button(
        label="📥 Descargar Proyecto (.zip)",
        data=zip_buffer.getvalue(),
        file_name=f"{project_name}.zip",
        mime="application/zip",
    )

PROJECTS_FILE_PATH = os.path.join("projects", "generated_projects.json")

def load_generated_projects() -> list[str]:
    """
    Carga la lista de nombres de proyectos generados desde un archivo JSON.
    
    Returns:
        Una lista de nombres de proyectos.
    """
    if not os.path.exists(PROJECTS_FILE_PATH):
        return []
    try:
        with open(PROJECTS_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_generated_projects(projects_list: list[str]):
    """
    Guarda la lista de nombres de proyectos generados en un archivo JSON.
    
    Args:
        projects_list: La lista de nombres de proyectos a guardar.
    """
    os.makedirs(os.path.dirname(PROJECTS_FILE_PATH), exist_ok=True)
    with open(PROJECTS_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(projects_list, f, indent=2)
