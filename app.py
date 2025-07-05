import streamlit as st
import subprocess
import json
import re
import os
import unicodedata
from pathlib import Path
from agents import PlannerAgent, CodeGeneratorAgent

def sanitize_filename(filename):
    """
    Sanitize a string to be used as a filename.
    Removes or replaces invalid characters and ensures the filename is safe for all operating systems.
    """
    # Remove accents and normalize unicode characters
    filename = str(filename)  # Ensure it's a string
    filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    
    # Replace invalid characters with underscores
    filename = re.sub(r'[<>:"/\\|?*%]', '_', filename)
    
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Ensure the filename is not empty
    if not filename:
        filename = 'unnamed_file'
    
    # Truncate if too long (max 255 chars is a safe limit for most filesystems)
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255 - len(ext)] + ext
    
    return filename

# Inicializar variables de sesión
if 'model_name' not in st.session_state:
    st.session_state.model_name = None

from utils import (
    StreamlitCallbackHandler, 
    download_project, 
    save_project,
    load_generated_projects,
    save_generated_projects
)
import os
import subprocess
import sys

st.set_page_config(page_title="VibeFactory - Fábrica de Software IA", layout="wide")

st.title("VibeFactory 🤖")
st.caption("Una Fábrica de Software 100% Automatizada con IA")

# --- Initialize Session State ---
if 'generated_projects' not in st.session_state:
    st.session_state.generated_projects = load_generated_projects()
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'tasks_generated' not in st.session_state:
    st.session_state.tasks_generated = False
if 'action_log' not in st.session_state:
    st.session_state.action_log = []

def get_installed_models():
    """Obtiene la lista de modelos instalados localmente en Ollama"""
    try:
        # First try with JSON format
        result = subprocess.run(['ollama', 'list', '--format', 'json'], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0 and result.stdout.strip():
            try:
                models = json.loads(result.stdout)
                if isinstance(models, list) and models:
                    # Return full model names with tags
                    return list(set(model['name'] for model in models))
            except json.JSONDecodeError:
                # If JSON parsing fails, try parsing the text output
                pass
        
        # Fallback to plain text output
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0 and result.stdout.strip():
            # Parse the text output
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                parts = line.split()
                if parts:  # Make sure line is not empty
                    model_name = parts[0]  # Get full name with tag
                    models.append(model_name)
            return list(set(models))  # Remove duplicates
            
        return []
    except Exception as e:
        st.error(f"Error al obtener modelos de Ollama: {e}")
        return []

# --- Sidebar for API Keys and Generated Projects ---
with st.sidebar:
    st.header("Configuración")
    
    # Get installed models
    installed_models = get_installed_models()
    if not installed_models:
        st.error("No se encontraron modelos de Ollama instalados. Por favor instala al menos un modelo (ej: 'ollama pull tinyllama').")
        st.stop()

    # Ensure we have a default model that exists
    default_model = 'tinyllama' if 'tinyllama' in installed_models else installed_models[0]

    # Initialize model_name in session state if not present
    if 'model_name' not in st.session_state:
        st.session_state.model_name = default_model

    # Select model
    selected_model = st.selectbox(
        "Selecciona el modelo de Ollama",
        installed_models,
        index=installed_models.index(st.session_state.model_name) if st.session_state.model_name in installed_models else 0
    )

    # Update session state if model was changed
    if selected_model != st.session_state.model_name:
        st.session_state.model_name = selected_model
        st.rerun()

    # Show current model and available models
    st.write(f"Usando modelo: {st.session_state.model_name}")
    st.caption(f"Modelos disponibles: {', '.join(installed_models)}")
    
    if not st.session_state.model_name:
            st.warning("Por favor, selecciona un modelo de Ollama para continuar.")

    st.header("Proyectos Generados")
    if not st.session_state.generated_projects:
        st.info("Aún no se han generado proyectos.")
    else:
        for project_name in st.session_state.generated_projects:
            if st.button(f"Ejecutar '{project_name}'"):
                project_path = os.path.join("projects", project_name, "app.py")
                if os.path.exists(project_path):
                    # Open a new terminal to run the app
                    command = f'streamlit run "{project_path}"'
                    if sys.platform == "win32":
                        subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', command])
                    else: # for macOS and Linux
                        subprocess.Popen(['x-terminal-emulator', '-e', command])
                    st.success(f"Iniciando '{project_name}' en una nueva terminal.")
                else:
                    st.error(f"No se encontró el archivo principal para '{project_name}'.")


# --- Main Area ---
main_col, log_col = st.columns([3, 1])

with log_col:
    st.header("📝 Log de Acciones")
    log_container = st.container()
    if st.session_state.action_log:
        for log_entry in st.session_state.action_log:
            log_container.info(log_entry)
    else:
        log_container.info("Esperando acciones...")

with main_col:
    project_description = st.text_area(
        "Describe tu proyecto aquí...",
        height=150,
        placeholder="Ej: Un MVP de una app para aprender SQL mediante juegos interactivos y desafíos."
    )

    project_name_input = st.text_input("Dale un nombre a tu proyecto (ej: gps_app)")

    if st.button("1. Generar Plan de Tareas", disabled=not st.session_state.get('model_name') or not project_name_input):
        if not project_description:
            st.error("La descripción del proyecto no puede estar vacía.")
        else:
            st.session_state.action_log = ["Iniciando planificación..."]
            with st.spinner("Inicializando agentes con Ollama..."):
                model = st.session_state.get('model_name')
                if not model:
                    st.error("No se ha seleccionado ningún modelo. Por favor selecciona un modelo de Ollama.")
                    st.stop()
                
                planner = PlannerAgent(model)
                code_generator = CodeGeneratorAgent(model)
            
            with st.spinner("Generando plan de tareas..."):
                # The callback handler is now less important for direct display
                tasks = planner.generate_tasks(project_description, callbacks=[])
            
            if tasks:
                st.session_state.tasks = tasks
                st.session_state.tasks_generated = True
                # Debug info
                print(f"Tasks generated: {tasks}")
                st.session_state.action_log.append(f"Tareas generadas: {len(tasks)} tareas")
                st.session_state.action_log.append("✅ Planificación completada.")
                st.rerun()
            else:
                st.error("El Agente Planificador no pudo generar tareas. Intenta de nuevo.")
                st.session_state.tasks_generated = False
                st.session_state.action_log.append("❌ Error en la planificación.")

    if st.session_state.tasks_generated and 'tasks' in st.session_state and st.session_state.tasks:
        st.header("📋 Plan de Tareas (Selecciona para generar)")
        
        # Debug info
        st.session_state.action_log.append(f"Tareas a mostrar: {len(st.session_state.tasks)}")
        
        # Initialize task tracking in session state
        if 'task_ids' not in st.session_state or 'task_id_to_text' not in st.session_state:
            st.session_state.task_ids = list(range(len(st.session_state.tasks)))
            st.session_state.task_id_to_text = {i: task for i, task in enumerate(st.session_state.tasks)}
            st.session_state.selected_tasks = {i: True for i in st.session_state.task_ids}
            # Create a list of unique task IDs and a mapping to tasks
            st.session_state.task_ids = list(range(len(st.session_state.tasks)))
            st.session_state.task_id_to_text = {i: task for i, task in enumerate(st.session_state.tasks)}
            st.session_state.selected_tasks = {i: True for i in st.session_state.task_ids}

        # "Select All" checkbox
        select_all = st.checkbox(
            "Seleccionar todas las tareas",
            value=all(st.session_state.selected_tasks.values()),
            key="select_all_tasks"
        )
        
        # Update all task selections if "Select All" was toggled
        if select_all != all(st.session_state.selected_tasks.values()):
            for task_id in st.session_state.task_ids:
                st.session_state.selected_tasks[task_id] = select_all
            st.rerun()  # Force a rerun to update the checkboxes

        # Display tasks with checkboxes
        for task_id in st.session_state.task_ids:
            task_text = st.session_state.task_id_to_text[task_id]
            # Use a unique key based on task_id instead of task text
            is_selected = st.checkbox(
                task_text,
                value=st.session_state.selected_tasks.get(task_id, True),
                key=f"task_{task_id}"  # Use task_id for unique key
            )
            st.session_state.selected_tasks[task_id] = is_selected

        if st.button("2. Generar Código para Tareas Seleccionadas 🚀", disabled=not any(st.session_state.selected_tasks.values())):
            project_name = project_name_input.replace(" ", "_").lower()
            model = st.session_state.get('model_name')
            if not model:
                st.error("No se ha seleccionado ningún modelo. Por favor selecciona un modelo de Ollama.")
                st.stop()
            code_generator = CodeGeneratorAgent(model_name=model)
            
            st.header("🤖 Código Generado")
            generated_files = {}
            # Convert selected task IDs back to task texts
            tasks_to_run = [
                st.session_state.task_id_to_text[task_id] 
                for task_id, selected in st.session_state.selected_tasks.items() 
                if selected and task_id in st.session_state.task_id_to_text
            ]
            st.session_state.action_log.append("Iniciando generación de código para tareas seleccionadas...")
            
            for task in tasks_to_run:
                if not task:
                    continue
                
                st.session_state.action_log.append(f"🔄 Trabajando en: {task}")
                # st.rerun() # This was causing the issue

                with st.expander(f"Tarea: {task}", expanded=True):
                    st.info(f"Agente Generador de Código trabajando en: {task}")
                    
                    # --- Streaming Code Generation ---
                    code_placeholder = st.empty()
                    full_response = ""
                    stream = code_generator.stream_code(
                        task,
                        project_description,
                        callbacks=[]
                    )
                    for chunk in stream:
                        full_response += chunk
                        # Display raw markdown for better formatting of non-code files
                        code_placeholder.markdown(full_response)
                    
                    # Parse the generated code
                    code_snippets = code_generator.parse_code(full_response)
                    
                    if code_snippets:
                        st.session_state.action_log.append(f"   -> Contenido generado y parseado para '{task}'")
                        
                        # Save the generated code
                        for filename, content in code_snippets.items():
                            if not filename.endswith(('.py', '.md', '.txt')):
                                filename += '.py'  # Default to .py if no extension
                            
                            # Create project directory if it doesn't exist
                            os.makedirs(project_name, exist_ok=True)
                            
                            try:
                                # Sanitize the filename
                                filename = sanitize_filename(filename)
                                
                                # Ensure we have a valid extension
                                if not any(filename.lower().endswith(ext) for ext in ['.py', '.md', '.txt', '.html', '.css', '.js']):
                                    filename += '.py'  # Default to .py if no valid extension
                                
                                # Create project directory if it doesn't exist
                                os.makedirs(project_name, exist_ok=True)
                                
                                # Create a safe file path
                                safe_filename = sanitize_filename(filename)
                                filepath = Path(project_name) / safe_filename
                                
                                # Ensure we're not writing outside the project directory
                                filepath = filepath.resolve()
                                if not str(filepath).startswith(str(Path(project_name).resolve())):
                                    raise ValueError(f"Ruta de archivo inválida: {filepath}")
                                
                                # Write the file with UTF-8 encoding
                                with open(filepath, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                
                                generated_files[filename] = content
                                st.session_state.action_log.append(f"✅ Archivo guardado: {filepath}")
                                
                                # If it's a Python file and the main app file, add it to the list of files to run
                                if filename.endswith('.py') and ('app.py' in filename or 'main.py' in filename):
                                    st.session_state.app_to_run = str(filepath)
                                    
                            except Exception as e:
                                st.error(f"❌ Error al guardar el archivo '{filename}': {str(e)}")
                                st.session_state.action_log.append(f"❌ Error al guardar '{filename}': {str(e)}")
                                continue  # Continue with the next file
                                
                                # Run the application if we found a main file
                                try:
                                    st.success("¡Aplicación generada con éxito!")
                                    st.info("Ejecutando la aplicación...")
                                    
                                    # Run the application in a subprocess
                                    process = subprocess.Popen(
                                        ['python', filepath],
                                        cwd=os.path.dirname(os.path.abspath(filepath)),
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True
                                    )
                                    
                                    # Install dependencies if requirements.txt exists
                                    project_dir = os.path.dirname(os.path.abspath(filepath))
                                    requirements_path = os.path.join(project_dir, 'requirements.txt')
                                    
                                    if os.path.exists(requirements_path):
                                        with st.spinner("Instalando dependencias..."):
                                            try:
                                                # Try with pip first
                                                install_cmd = [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']
                                                install_process = subprocess.Popen(
                                                    install_cmd,
                                                    cwd=project_dir,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    text=True
                                                )
                                                
                                                # Show installation progress
                                                install_output = []
                                                while True:
                                                    output = install_process.stderr.readline()
                                                    if output == '' and install_process.poll() is not None:
                                                        break
                                                    if output:
                                                        install_output.append(output.strip())
                                                
                                                install_success = install_process.returncode == 0
                                                if install_success:
                                                    st.session_state.action_log.append("✅ Dependencias instaladas correctamente")
                                                else:
                                                    st.warning("Hubo un problema instalando las dependencias")
                                                    st.session_state.action_log.append("⚠️ Error al instalar dependencias:")
                                                    for line in install_output:
                                                        st.session_state.action_log.append(f"   {line}")
                                                        
                                            except Exception as e:
                                                st.error(f"Error al instalar dependencias: {str(e)}")
                                                st.session_state.action_log.append(f"❌ Error al instalar dependencias: {str(e)}")
                                    
                                    # Run the application
                                    with st.spinner("Iniciando la aplicación..."):
                                        try:
                                            # Try different Python commands if needed
                                            python_commands = [sys.executable, 'python3', 'python']
                                            process = None
                                            
                                            for cmd in python_commands:
                                                try:
                                                    process = subprocess.Popen(
                                                        [cmd, os.path.basename(filepath)],
                                                        cwd=project_dir,
                                                        stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE,
                                                        text=True,
                                                        bufsize=1,
                                                        universal_newlines=True
                                                    )
                                                    break  # Successfully started the process
                                                except (FileNotFoundError, OSError):
                                                    continue
                                            
                                            if process is None:
                                                raise RuntimeError("No se pudo encontrar un intérprete de Python válido")
                                            
                                            # Show the output in the UI
                                            output_placeholder = st.empty()
                                            output_lines = []
                                            
                                            while True:
                                                output = process.stdout.readline()
                                                if output == '' and process.poll() is not None:
                                                    break
                                                if output:
                                                    output_lines.append(output.strip())
                                                    output_placeholder.text("\n".join(output_lines[-10:]))  # Show last 10 lines
                                            
                                            # Check for errors
                                            _, stderr = process.communicate()
                                            if process.returncode != 0:
                                                st.error(f"La aplicación finalizó con código de error {process.returncode}")
                                                if stderr:
                                                    st.session_state.action_log.append("⚠️ Errores de la aplicación:")
                                                    for line in stderr.splitlines():
                                                        st.session_state.action_log.append(f"   {line}")
                                            else:
                                                st.success("¡Aplicación ejecutada con éxito!")
                                                
                                        except Exception as e:
                                            error_msg = f"Error al ejecutar la aplicación: {str(e)}"
                                            st.error(error_msg)
                                            st.session_state.action_log.append(f"❌ {error_msg}")
                                    
                                except Exception as e:
                                    st.error(f"Error al ejecutar la aplicación: {str(e)}")
                    else:
                        st.warning("No se pudo generar código para esta tarea.")
                        st.session_state.action_log.append(f"   -> ⚠️ No se generó código para '{task}'")
            
            st.session_state.action_log.append("✅ Generación de código completada.")
            st.rerun()
            
            if generated_files:
                st.header("✅ Proyecto Generado")
                st.session_state.action_log.append("Guardando proyecto...")
                save_project(project_name, generated_files)
                st.success(f"¡Proyecto '{project_name}' guardado en la carpeta 'projects'!")
                st.session_state.action_log.append(f"✅ Proyecto '{project_name}' guardado.")

                if project_name not in st.session_state.generated_projects:
                    st.session_state.generated_projects.append(project_name)
                    save_generated_projects(st.session_state.generated_projects)
                
                download_project(generated_files, project_name)
                
                # Reset state for next generation
                st.session_state.action_log.append("Limpiando para la próxima generación...")
                st.session_state.tasks = []
                st.session_state.tasks_generated = False
                st.rerun()
            else:
                st.error("No se pudo generar ningún archivo. Revisa las tareas y vuelve a intentarlo.")
