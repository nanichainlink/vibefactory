"""
Script para configurar el entorno de desarrollo.

Este script instala las dependencias necesarias y configura pre-commit.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command: str, cwd: str = None) -> bool:
    """Ejecuta un comando en la terminal."""
    try:
        print(f"Ejecutando: {command}")
        result = subprocess.run(
            command,
            cwd=cwd or os.getcwd(),
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    # Verificar que estamos en el directorio correcto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("\n=== Configuración del entorno de desarrollo ===\n")
    
    # 1. Actualizar pip
    print("\n1. Actualizando pip...")
    if not run_command("python -m pip install --upgrade pip"):
        print("\nError al actualizar pip. Saliendo...")
        sys.exit(1)
    
    # 2. Instalar dependencias de desarrollo
    print("\n2. Instalando dependencias de desarrollo...")
    if not run_command("pip install -r requirements-dev.txt"):
        print("\nError al instalar dependencias de desarrollo. Saliendo...")
        sys.exit(1)
    
    # 3. Instalar pre-commit
    print("\n3. Instalando pre-commit...")
    if not run_command("pip install pre-commit"):
        print("\nError al instalar pre-commit. Saliendo...")
        sys.exit(1)
    
    # 4. Configurar pre-commit
    print("\n4. Configurando pre-commit...")
    if not run_command("pre-commit install"):
        print("\nError al configurar pre-commit. Saliendo...")
        sys.exit(1)
    
    # 5. Instalar hooks de pre-commit
    print("\n5. Instalando hooks de pre-commit...")
    if not run_command("pre-commit install --install-hooks"):
        print("\nError al instalar hooks de pre-commit. Saliendo...")
        sys.exit(1)
    
    print("\n¡Configuración completada con éxito!")
    print("El entorno de desarrollo está listo para usar.")

if __name__ == "__main__":
    main()
