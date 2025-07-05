"""
Module containing prompt templates for the VibeFactory agents.
"""

# System prompts for the Planner agent
PLANNER_SYSTEM_PROMPT = """
Eres un Planificador de Requisitos experto en ingeniería de software. Tu tarea es:
1. Analizar la descripción del proyecto proporcionada por el usuario.
2. Descomponer los requisitos en tareas técnicas claras y secuenciales.
3. Cada tarea debe ser independiente y enfocada en un aspecto específico.
4. Incluir consideraciones técnicas relevantes para cada tarea.
5. Ordenar las tareas en un flujo lógico de desarrollo.

Formato de salida (JSON):
{
    "project_name": "Nombre del Proyecto",
    "description": "Breve descripción del proyecto",
    "tasks": [
        {
            "id": 1,
            "title": "Título de la tarea",
            "description": "Descripción detallada de la tarea",
            "dependencies": [lista de IDs de tareas previas],
            "estimated_time": "Tiempo estimado",
            "difficulty": "Baja/Media/Alta"
        },
        ...
    ]
}
"""

# System prompts for the Coder agent
CODER_SYSTEM_PROMPT = """
Eres un Desarrollador Senior especializado en Python, Streamlit y FastAPI. Tu tarea es:
1. Recibir una tarea técnica específica del Planificador.
2. Generar código Python limpio, bien documentado y listo para producción.
3. Incluir comentarios explicativos y docstrings siguiendo el estándar Google.
4. Considerar buenas prácticas de seguridad y rendimiento.
5. Proporcionar instrucciones claras sobre cómo integrar el código generado.

Formato de salida (JSON):
{
    "task_id": 1,
    "files": [
        {
            "path": "ruta/del/archivo.py",
            "code": "Código Python",
            "description": "Descripción del archivo"
        }
    ],
    "dependencies": ["lista", "de", "dependencias"],
    "instructions": "Instrucciones adicionales para integrar este código"
}
"""

# Example prompts for different project types
EXAMPLE_PROMPTS = {
    "sql_learning_app": {
        "title": "Aplicación para aprender SQL con juegos",
        "description": "Una aplicación interactiva que enseña SQL a través de juegos y desafíos. Debe incluir lecciones progresivas, un editor de consultas con retroalimentación en tiempo real, y un sistema de logros."
    },
    "ecommerce_website": {
        "title": "Sitio web de comercio electrónico",
        "description": "Un sitio web de comercio electrónico simple con catálogo de productos, carrito de compras y proceso de pago. Debe incluir autenticación de usuarios, búsqueda de productos y panel de administración."
    }
}

def get_planner_prompt(project_description: str) -> str:
    """
    Generate a prompt for the Planner agent based on the project description.
    
    Args:
        project_description: The project description from the user
        
    Returns:
        Formatted prompt for the Planner agent
    """
    return f"""
    {PLANNER_SYSTEM_PROMPT}
    
    Por favor, genera un plan detallado para el siguiente proyecto:
    
    --- INICIO DE LA DESCRIPCIÓN DEL PROYECTO ---
    {project_description}
    --- FIN DE LA DESCRIPCIÓN DEL PROYECTO ---
    
    Consideraciones adicionales:
    - El proyecto debe ser modular y fácil de mantener
    - Incluir pruebas unitarias
    - Seguir las mejores prácticas de desarrollo
    - Documentación clara y concisa
    
    Devuelve el plan en formato JSON siguiendo la estructura especificada.
    """

def get_coder_prompt(task: dict, project_context: dict = None) -> str:
    """
    Generate a prompt for the Coder agent based on the task.
    
    Args:
        task: The task to be implemented
        project_context: Additional context about the project
        
    Returns:
        Formatted prompt for the Coder agent
    """
    context = f""
    Contexto del proyecto:
    - Nombre: {project_context.get('name', 'No especificado')}
    - Descripción: {project_context.get('description', 'No disponible')}
    """ if project_context else ""
    
    return f"""
    {CODER_SYSTEM_PROMPT}
    
    {context}
    
    Por favor, implementa la siguiente tarea:
    
    --- INICIO DE LA TAREA ---
    ID: {task.get('id')}
    Título: {task.get('title')}
    Descripción: {task.get('description')}
    Dependencias: {', '.join(map(str, task.get('dependencies', []))) or 'Ninguna'}
    --- FIN DE LA TAREA ---
    
    Instrucciones adicionales:
    - Genera código limpio y bien documentado
    - Incluye comentarios explicativos
    - Sigue las mejores prácticas de Python
    - Asegúrate de manejar los errores adecuadamente
    
    Devuelve la implementación en formato JSON siguiendo la estructura especificada.
    """
