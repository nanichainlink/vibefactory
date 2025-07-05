# Estructura del Proyecto VibeFactory

Este documento describe la estructura de directorios y archivos del proyecto VibeFactory, una fábrica de software automatizado con IA.

## Visión General

```
vibefactory/
├── .github/                  # Configuración de GitHub (workflows, templates)
│   └── workflows/            # Pipelines de CI/CD
├── .windsurf/               # Configuración específica de VibeFactory
│   ├── metrics/             # Métricas y estadísticas
│   └── templates/           # Plantillas de prompts
├── api/                     # Endpoints FastAPI
│   ├── __init__.py
│   ├── endpoints.py         # Definición de endpoints
│   └── models.py            # Modelos Pydantic
├── services/                # Lógica de negocio
│   ├── __init__.py
│   ├── orchestrator.py      # Orquestador de agentes
│   └── project_service.py   # Gestión de proyectos
├── static/                  # Archivos estáticos
│   └── css/
│       └── styles.css
├── templates/               # Plantillas HTML
│   └── email/
├── tests/                   # Pruebas
│   ├── unit/               # Pruebas unitarias
│   └── integration/        # Pruebas de integración
├── .env.example            # Variables de entorno de ejemplo
├── agents.py               # Agentes IA (Planificador y Generador)
├── app.py                  # Aplicación principal Streamlit
├── config.py               # Configuración de la aplicación
├── models.py               # Modelos de datos
└── utils.py                # Utilidades
```

## Descripción Detallada

### Directorio Raíz

- `app.py`: Punto de entrada principal de la aplicación Streamlit.
- `agents.py`: Implementación de los agentes IA (Planificador y Generador de Código).
- `models.py`: Definición de los modelos de datos principales.
- `utils.py`: Funciones de utilidad y helpers.
- `config.py`: Configuración de la aplicación.
- `requirements.txt`: Dependencias principales del proyecto.
- `requirements-dev.txt`: Dependencias de desarrollo.
- `.pre-commit-config.yaml`: Configuración de pre-commit hooks.
- `.env.example`: Plantilla para variables de entorno.

### Directorio `api/`

Contiene la definición de los endpoints de la API REST y los modelos Pydantic.

- `endpoints.py`: Definición de los endpoints de la API.
- `models.py`: Modelos Pydantic para validación de datos.

### Directorio `services/`

Contiene la lógica de negocio principal.

- `orchestrator.py`: Orquesta la interacción entre los agentes IA.
- `project_service.py`: Gestiona la creación y manipulación de proyectos.

### Directorio `static/`

Archivos estáticos como CSS, JavaScript e imágenes.

### Directorio `templates/`

Plantillas HTML para correos electrónicos u otras salidas.

### Directorio `tests/`

Pruebas automatizadas del proyecto.

- `unit/`: Pruebas unitarias.
- `integration/`: Pruebas de integración.

## Flujo de Trabajo Recomendado

1. **Desarrollo Local**
   - Crear un entorno virtual: `python -m venv .venv`
   - Activar el entorno: `.venv\Scripts\activate` (Windows) o `source .venv/bin/activate` (Unix)
   - Instalar dependencias: `pip install -r requirements.txt -r requirements-dev.txt`
   - Configurar pre-commit: `pre-commit install`

2. **Ejecución**
   - Iniciar la aplicación: `streamlit run app.py`
   - Ejecutar pruebas: `pytest`
   - Verificar cobertura: `pytest --cov=vibefactory tests/`

3. **Despliegue**
   - Configurar variables de entorno en `.env`
   - Soportado despliegue en cualquier plataforma que soporte Python 3.10+

## Convenciones de Código

- **Documentación**: Docstrings en formato Google.
- **Estilo**: PEP 8 con type hints obligatorios.
- **Pruebas**: Cobertura mínima del 80%.
- **Commits**: Mensajes descriptivos siguiendo Conventional Commits.

## Seguridad

- No incluir credenciales en el código.
- Usar variables de entorno para datos sensibles.
- Validar todas las entradas de usuario.
- Mantener las dependencias actualizadas.

## Contribución

1. Hacer fork del repositorio
2. Crear una rama para la característica (`feature/descripcion`)
3. Hacer commit de los cambios
4. Hacer push a la rama
5. Abrir un Pull Request
