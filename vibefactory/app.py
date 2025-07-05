"""
VibeFactory - Fábrica de Software Automatizado IA

Este módulo es la aplicación principal de Streamlit que orquesta los agentes IA
para la generación de código basado en requisitos.
"""

import streamlit as st
from datetime import datetime, timedelta
import json
import os
import time
import uuid
from typing import Dict, List, Optional, Tuple

# Importar servicios
from services.orchestrator import Orchestrator

# Configuración de la página
st.set_page_config(
    page_title="VibeFactory",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar el orquestador (se mantiene en el estado de la sesión)
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None
if 'project_id' not in st.session_state:
    st.session_state.project_id = None
if 'generation_started' not in st.session_state:
    st.session_state.generation_started = False
if 'generation_complete' not in st.session_state:
    st.session_state.generation_complete = False
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "new_project"

# Título principal
st.title("🏭 VibeFactory")
st.caption("Tu fábrica de software automatizado con IA")

def init_orchestrator(api_key: str):
    """Inicializa el orquestador con la API key proporcionada."""
    if not st.session_state.orchestrator or st.session_state.api_key != api_key:
        st.session_state.orchestrator = Orchestrator(perplexity_api_key=api_key)
        st.session_state.api_key = api_key
        st.success("✅ Orquestador inicializado correctamente")
    return st.session_state.orchestrator

def format_timedelta(delta: timedelta) -> str:
    """Formatea un timedelta a un string legible."""
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Configuración de API Keys
    st.subheader("🔑 API Keys")
    perplexity_api_key = st.text_input(
        "Perplexity API Key",
        type="password",
        help="Ingresa tu API Key de Perplexity",
        key="perplexity_api_key_input"
    )
    
    # Configuración de parámetros
    st.subheader("⚡ Parámetros")
    temperature = st.slider("Temperatura", 0.1, 1.0, 0.7, 0.1,
                          help="Controla la creatividad de los agentes")
    
    # Estado de la aplicación
    st.divider()
    st.subheader("📊 Estado")
    st.metric("Proyectos Activos", "0")
    st.metric("Agentes Funcionando", "0/2")
    st.metric("Tiempo Promedio", "--")
    st.metric("Tasa de Éxito", "--%")

# Navegación por pestañas
tab1, tab2 = st.tabs(["🚀 Nuevo Proyecto", "📊 Panel de Control"])

with tab1:
    # Área principal de la aplicación
    st.header("🚀 Nuevo Proyecto")
    
    project_description = st.text_area(
        "Describe tu proyecto:",
        placeholder="Ej: 'Quiero una aplicación web para aprender SQL con juegos interactivos...'"
    )
    
    # Selección de tipo de proyecto
    project_type = st.selectbox(
        "Tipo de Proyecto:",
        ["web", "api", "data_science", "mobile", "desktop"],
        index=0,
        help="Selecciona el tipo de proyecto que deseas generar"
    )
    
    # Botón para generar MVP
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_button = st.button(
            "✨ Generar MVP",
            type="primary",
            disabled=not (project_description and perplexity_api_key),
            use_container_width=True
        )
    with col2:
        if st.session_state.generation_started and not st.session_state.generation_complete:
            if st.button("⏹️ Detener Generación", type="secondary", use_container_width=True):
                st.session_state.generation_started = False
                st.rerun()
    
    # Mostrar estado de la generación
    if st.session_state.generation_started and st.session_state.project_id:
        with st.status("🚀 Generando tu proyecto...", expanded=True) as status:
            if st.session_state.orchestrator and st.session_state.project_id:
                try:
                    project = st.session_state.orchestrator.get_project(st.session_state.project_id)
                    
                    # Mostrar progreso
                    total_tasks = len(project["tasks"])
                    completed_tasks = sum(1 for t in project["tasks"] if t["status"] == "completed")
                    progress = completed_tasks / total_tasks if total_tasks > 0 else 0
                    
                    st.progress(progress, text=f"Progreso: {completed_tasks}/{total_tasks} tareas completadas")
                    
                    # Mostrar tareas
                    st.subheader("📋 Tareas")
                    for task in project["tasks"]:
                        status_emoji = "✅" if task["status"] == "completed" else "⏳"
                        st.write(f"{status_emoji} {task['description']}")
                    
                    # Si hay tareas pendientes, procesar la siguiente
                    if not st.session_state.generation_complete and progress < 1.0:
                        next_task = next((t for t in project["tasks"] if t["status"] == "pending"), None)
                        if next_task:
                            try:
                                st.write(f"🔧 Procesando tarea: {next_task['description']}")
                                result = st.session_state.orchestrator.generate_task_code(
                                    project_id=st.session_state.project_id,
                                    task_id=next_task["id"]
                                )
                                
                                if result["status"] == "success":
                                    st.success(f"✅ Tarea {next_task['id']} completada")
                                    
                                    # Mostrar código generado
                                    with st.expander(f"Ver código generado para tarea {next_task['id']}"):
                                        st.code(result["code"], language="python")
                                
                                # Pequeña pausa para permitir la actualización de la UI
                                time.sleep(0.5)
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Error al procesar tarea: {str(e)}")
                                st.session_state.generation_complete = True
                        else:
                            st.session_state.generation_complete = True
                            st.balloons()
                            st.success("¡Proyecto generado con éxito! 🎉")
                    
                    # Si se completó la generación
                    if progress >= 1.0 and not st.session_state.generation_complete:
                        st.session_state.generation_complete = True
                        st.balloons()
                        st.success("¡Proyecto generado con éxito! 🎉")
                        
                        # Mostrar opciones de descarga
                        st.download_button(
                            label="⬇️ Descargar Proyecto",
                            data=json.dumps(project, indent=2, ensure_ascii=False),
                            file_name=f"vibefactory_{st.session_state.project_id}.json",
                            mime="application/json"
                        )
                
                except Exception as e:
                    st.error(f"Error al obtener información del proyecto: {str(e)}")
                    st.session_state.generation_complete = True
    
    # Manejador del botón de generación
    if generate_button and project_description and not st.session_state.generation_started:
        try:
            # Inicializar orquestador
            orchestrator = init_orchestrator(perplexity_api_key)
            
            # Crear nuevo proyecto
            project_id = str(uuid.uuid4())
            project = orchestrator.create_project(
                description=project_description,
                project_type=project_type
            )
            
            # Actualizar estado de la sesión
            st.session_state.project_id = project_id
            st.session_state.generation_started = True
            st.session_state.generation_complete = False
            st.rerun()
            
        except Exception as e:
            st.error(f"Error al iniciar la generación: {str(e)}")

with tab2:
    # Dashboard de métricas
    st.header("📊 Panel de Control")
    
    if st.session_state.orchestrator:
        metrics = st.session_state.orchestrator.get_metrics()
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Proyectos Totales", metrics["total_projects"])
        
        with col2:
            st.metric("Proyectos Activos", metrics["active_projects"])
        
        with col3:
            avg_time = metrics["avg_generation_time"]
            if avg_time > 0:
                avg_time_str = format_timedelta(timedelta(seconds=avg_time))
            else:
                avg_time_str = "--:--:--"
            st.metric("Tiempo Promedio", avg_time_str)
        
        with col4:
            st.metric("Tasa de Éxito", f"{metrics['success_rate']*100:.1f}%")
        
        # Sección de proyectos recientes
        st.subheader("📋 Proyectos Recientes")
        if st.session_state.orchestrator.active_projects:
            for project_id, project in st.session_state.orchestrator.active_projects.items():
                with st.expander(f"Proyecto: {project_id}"):
                    st.write(f"**Descripción:** {project['description']}")
                    st.write(f"**Estado:** {project['status']}")
                    st.write(f"**Creado:** {project['created_at']}")
                    
                    # Mostrar progreso
                    total_tasks = len(project["tasks"])
                    completed_tasks = sum(1 for t in project["tasks"] if t["status"] == "completed")
                    st.progress(
                        completed_tasks / total_tasks if total_tasks > 0 else 0,
                        text=f"{completed_tasks}/{total_tasks} tareas completadas"
                    )
        else:
            st.info("No hay proyectos activos en este momento.")
    else:
        st.warning("Inicia el orquestador ingresando una API key en la pestaña 'Nuevo Proyecto'.")

# Estilos CSS personalizados
st.markdown("""
    <style>
    .stButton>button {
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stTextArea textarea {
        min-height: 150px;
    }
    .metric-value {
        font-size: 1.5rem !important;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar el orquestador si hay una API key
if perplexity_api_key and not st.session_state.orchestrator:
    init_orchestrator(perplexity_api_key)
