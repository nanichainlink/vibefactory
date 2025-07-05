import streamlit as st
import zipfile
import io
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

def download_project(files: dict[str, str]):
    """
    Crea un botón de descarga en Streamlit para un proyecto generado.
    
    Args:
        files: Un diccionario donde las claves son nombres de archivo y los
               valores son el contenido del archivo.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, content in files.items():
            # Asegurarse de que el contenido sea bytes
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = content
            zip_file.writestr(file_name, content_bytes)

    st.download_button(
        label="📥 Descargar Proyecto (.zip)",
        data=zip_buffer.getvalue(),
        file_name="vibefactory_project.zip",
        mime="application/zip",
    )
