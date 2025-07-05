"""Módulo para el registro automático de acciones en el proyecto."""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

# Configuración
LOG_DIR = Path("docs")
ACTIONS_LOG = LOG_DIR / "actions_log.md"
DOCSTRINGS_LOG = LOG_DIR / "docstring_report.md"


def ensure_logs_dir() -> None:
    """Asegura que el directorio de logs exista."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_action(
    action_type: str,
    files_affected: List[Union[str, Path]],
    changes: List[str],
    metadata: Optional[Dict] = None,
) -> None:
    """Registra una acción en el archivo de logs.

    Args:
        action_type: Tipo de acción realizada (ej: 'Configuración', 'Documentación', etc.)
        files_affected: Lista de archivos afectados por la acción
        changes: Lista de descripciones de los cambios realizados
        metadata: Metadatos adicionales en formato diccionario
    """
    ensure_logs_dir()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Formatear lista de archivos afectados
    files_list = "\n".join(f"  - `{str(f)}`" for f in files_affected)
    
    # Formatear lista de cambios
    changes_list = "\n".join(f"  - {change}" for change in changes)
    
    # Formatear metadatos si existen
    metadata_section = ""
    if metadata:
        metadata_str = json.dumps(metadata, indent=2, ensure_ascii=False)
        metadata_section = f"\n- **Metadatos**:\n  ```json\n{metadata_str}\n  ```"
    
    # Crear entrada de log
    log_entry = f"""
### {timestamp} - {action_type}
- **Archivos Afectados**:
{files_list}
- **Cambios Realizados**:
{changes_list}{metadata_section}
"""
    # Asegurar que el archivo exista
    if not ACTIONS_LOG.exists():
        with open(ACTIONS_LOG, 'w', encoding='utf-8') as f:
            f.write("# Registro de Acciones Automáticas\n\n")
            f.write("Este archivo registra automáticamente todas las acciones realizadas "
                   "por el sistema de automatización.\n\n")
            f.write("## Formato\n\n")
            f.write("```\n### [YYYY-MM-DD HH:MM:SS UTC] - [Tipo de Acción]\n")
            f.write("- **Archivos Afectados**: \n  - `ruta/al/archivo`\n")
            f.write("- **Cambios Realizados**:\n  - Descripción detallada de los cambios\n```\n\n---\n")
    
    # Añadir entrada al inicio del archivo
    with open(ACTIONS_LOG, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(content.replace("---\n", f"---\n{log_entry}"))


def update_docstring_report(module_path: str, stats: Dict[str, int]) -> None:
    """Actualiza el reporte de docstrings.

    Args:
        module_path: Ruta al módulo (ej: 'src/core/task_runner.py')
        stats: Estadísticas de documentación del módulo
    """
    ensure_logs_dir()
    
    # Crear archivo si no existe
    if not DOCSTRINGS_LOG.exists():
        with open(DOCSTRINGS_LOG, 'w', encoding='utf-8') as f:
            f.write("# Reporte de Docstrings\n\n")
            f.write("Este archivo rastrea automáticamente la documentación de "
                   "funciones y clases en el proyecto.\n\n")
            f.write("## Estándar de Documentación\n\n")
            f.write("El proyecto sigue el formato Google para docstrings:\n\n")
            f.write("```python\n")
            f.write('def funcion_ejemplo(param1: tipo, param2: tipo = valor) -> tipo_retorno:\n')
            f.write('    \"\"\"Descripción breve de una línea.\n\n')
            f.write('    Descripción detallada que puede abarcar múltiples líneas.\n\n')
            f.write('    Args:\n')
            f.write('        param1: Descripción del primer parámetro.\n')
            f.write('        param2: Descripción del segundo parámetro. Por defecto es valor.\n\n')
            f.write('    Returns:\n')
            f.write('        Descripción del valor de retorno.\n\n')
            f.write('    Raises:\n')
            f.write('        TipoError: Descripción de cuándo se lanza.\n')
            f.write('    \"\"\"\n')
            f.write('    pass\n')
            f.write('```\n\n## Módulos Revisados\n\n')
            f.write("## Estadísticas\n\n")
            f.write("- **Total de funciones**: 0\n")
            f.write("- **Total de clases**: 0\n")
            f.write("- **Funciones documentadas**: 0\n")
            f.write("- **Clases documentadas**: 0\n")
            f.write("- **Porcentaje de documentación**: 0%\n\n")
            f.write("## Próximos Pasos\n\n")
            f.write("1. Revisar y documentar módulos principales\n")
            f.write("2. Actualizar estadísticas de documentación\n\n")
            f.write("---\n\n")
            f.write("*Última actualización: 2025-07-01 02:42:42 UTC*  \n")
            f.write("*Este archivo se actualiza automáticamente. No editar manualmente.*\n")
    
    # Actualizar la última fecha de modificación
    with open(DOCSTRINGS_LOG, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Actualizar la fecha de última actualización
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    content = content.replace(
        "*Última actualización: ", 
        f"*Última actualización: {timestamp}*  \n"
    )
    
    with open(DOCSTRINGS_LOG, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    # Ejemplo de uso
    log_action(
        action_type="Prueba",
        files_affected=["test_file1.py", "test_file2.py"],
        changes=["Se agregó función de prueba", "Se corrigió error de importación"],
        metadata={"usuario": "sistema", "origen": "test_logging"}
    )
