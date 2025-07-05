# Guía de Prompts para VibeFactory

Esta guía explica cómo crear y utilizar prompts efectivos con los agentes de VibeFactory.

## Estructura de un Prompt

Un buen prompt para VibeFactory debe incluir:

1. **Contexto**: Breve descripción del objetivo
2. **Instrucciones**: Pasos específicos para el agente
3. **Formato de salida**: Estructura esperada
4. **Ejemplos**: Si es necesario para guiar la respuesta

## Directorios

- `planner/`: Ejemplos para el agente Planificador
- `generator/`: Ejemplos para el agente Generador de Código

## Mejores Prácticas

- Sé específico y claro en las instrucciones
- Proporciona ejemplos cuando sea necesario
- Especifica el formato de salida deseado
- Incluye restricciones o requisitos específicos
- Mantén los prompts modulares y reutilizables

## Uso Básico

```python
from vibefactory import Planificador, GeneradorCodigo

# Inicializar el planificador
planificador = Planificador(api_key="tu_api_key")

# Usar un prompt del planificador
response = planificador.generar_plan(
    project_name="Mi Proyecto",
    project_description="Una aplicación web para gestión de tareas",
    requirements=["Autenticación de usuarios", "CRUD de tareas"],
    target_tech=["Python", "FastAPI", "React"]
)
```
