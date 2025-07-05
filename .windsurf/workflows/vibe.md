---
trigger: always_on
description: # Metodología Vibe Coding + Workflow 24/7
---

Description
A description for this workflow (Maximum 250 characters)
Content
# Metodología Vibe Coding + Workflow 24/7

## Visión General

La metodología Vibe Coding combina la generación de código con IA y la validación humana en ciclos rápidos, integrada con un flujo de trabajo 24/7 para entrega continua.

## Fase 1: Preparación y Configuración Inicial

### 1.1 Definición de Plantillas de Prompt

```python
# Ejemplo de plantilla de prompt en .windsurf/templates/prompt_template.py
def create_prompt(requirement: str, context: dict) -> str:
    """
    Genera un prompt estructurado para la generación de código.
    
    Args:
        requirement: Requisito funcional a implementar
        context: Contexto adicional (ej: stack tecnológico, patrones de diseño)
    """
    return f"""
    # Contexto del Proyecto
    - Stack Tecnológico: {context.get('tech_stack', 'Python 3.10+')}
    - Patrones de Diseño: {', '.join(context.get('design_patterns', ['Clean Code']))}
    - Estilo de Código: {context.get('code_style', 'PEP 8')}
    
    # Requisito a Implementar
    {requirement}
    
    Por favor, genera el código siguiendo estos lineamientos:
    1. Incluye documentación clara
    2. Añade tipos de datos estáticos
    3. Sigue principios SOLID
    4. Incluye manejo de errores
    5. Proporciona ejemplos de uso
    """
```

### 1.2 Configuración del Entorno de IA

```yaml
# .windsurf/ai_config.yaml
models:
  default: "gpt-4-turbo"
  fallback: "gpt-3.5-turbo"
  code_review: "claude-3-opus"

temperature:
  code_generation: 0.2
  idea_generation: 0.7
  testing: 0.3

context_window: 16000
max_tokens: 4000
```

### 1.3 Configuración de Herramientas Base

```bash
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
    - id: black
      language_version: python3.10

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
        name: isort (python)
        args: [--profile=black]
```

## Fase 2: Sesión de Prompt Engineering

### 2.1 Plantilla de Especificación de Requisitos

```markdown
## Especificación de Requisito

### Contexto
[Descripción del contexto del requisito]

### Requisito Funcional
[Descripción clara del requisito]

### Criterios de Aceptación
- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Criterio 3

### Restricciones Técnicas
- [ ] Restricción 1
- [ ] Restricción 2

### Ejemplos
```python
# Ejemplo de uso esperado
```
```

## Fase 3: Generación Interactiva de Código

### 3.1 Script de Generación de Código

```python
# scripts/generate_code.py
import openai
import yaml
from pathlib import Path
from typing import Dict, Any

def load_ai_config() -> Dict[str, Any]:
    config_path = Path(".windsurf/ai_config.yaml")
    return yaml.safe_load(config_path.read_text())

def generate_with_ai(prompt: str, context: Dict[str, Any]) -> str:
    config = load_ai_config()
    
    response = openai.ChatCompletion.create(
        model=config["models"]["default"],
        messages=[
            {"role": "system", "content": "Eres un asistente de programación experto."},
            {"role": "user", "content": prompt}
        ],
        temperature=config["temperature"]["code_generation"],
        max_tokens=config["max_tokens"]
    )
    
    return response.choices[0].message.content

# Uso en el IDE/CLI
if __name__ == "__main__":
    context = {
        "tech_stack": "Python 3.10, FastAPI, SQLAlchemy",
        "design_patterns": ["Repository", "Dependency Injection"],
        "code_style": "PEP 8 con type hints"
    }
    
    requirement = input("Ingrese el requisito a implementar: ")
    prompt = create_prompt(requirement, context)
    generated_code = generate_with_ai(prompt, context)
    print("\nCódigo generado:")
    print(generated_code)
```

## Fase 4: Revisión y Validación Humana

### 4.1 Checklist de Revisión de Código

```markdown
# Checklist de Revisión de Código

## Calidad de Código
- [ ] El código sigue las guías de estilo del proyecto
- [ ] Los nombres de variables y funciones son descriptivos
- [ ] No hay código duplicado
- [ ] El código es modular y sigue principios SOLID

## Seguridad
- [ ] No hay vulnerabilidades de seguridad evidentes
- [ ] Se manejan adecuadamente los datos sensibles
- [ ] Se validan todas las entradas de usuario

## Rendimiento
- [ ] No hay operaciones bloqueantes innecesarias
- [ ] Las consultas a la base de datos son óptimas
- [ ] Se manejan adecuadamente los recursos del sistema

## Pruebas
- [ ] El código incluye pruebas unitarias
- [ ] Las pruebas cubren los casos de uso principales
- [ ] Se han probado casos límite
```

## Fase 5: Generación Automática de Pruebas

### 5.1 Script de Generación de Pruebas

```python
# scripts/generate_tests.py
import ast
import astor
import openai
from typing import List, Dict, Any

def generate_test_cases(code: str, context: Dict[str, Any]) -> str:
    prompt = f"""
    Genera casos de prueba unitarios para el siguiente código Python.
    Incluye casos de prueba para:
    1. Comportamiento normal
    2. Casos límite
    3. Manejo de errores
    
    Código a probar:
    ```python
    {code}
    ```
    
    Contexto: {context}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un experto en pruebas de software."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def extract_functions(code: str) -> List[ast.FunctionDef]:
    """Extrae las definiciones de funciones del código."""
    tree = ast.parse(code)
    return [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
```

## Fase 6: Integración con Workflow 24/7

### 6.1 Configuración de GitHub Actions

```yaml
# .github/workflows/24_7_vibe_coding.yml
name: Vibe Coding 24/7

on:
  schedule:
    - cron: '*/5 * * * *'  # Ejecutar cada 5 minutos
  workflow_dispatch:
  push:
    branches: [ main ]
    paths-ignore:
      - '**.md'
      - '**.txt'
      - '.github/**'

jobs:
  vibe-coding:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
          
      - name: Run Vibe Coding Workflow
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python -m scripts.vibe_coding_workflow
          
      - name: Run Tests
        run: |
          python -m pytest tests/unit tests/integration -v
          
      - name: Code Quality Check
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          black --check .
          
      - name: Commit Changes
        if: success()
        run: |
          git config --local user.email "vibe-coding@conectatech.com"
          git config --local user.name "Vibe Coding Bot"
          git add .
          git diff-index --quiet HEAD || \
            (git commit -m "[VIBE] Actualización automática de código" && \
             git push origin main)
```

## Fase 7: Retroalimentación y Mejora Continua

### 7.1 Panel de Métricas

```python
# scripts/metrics_dashboard.py
import json
from datetime import datetime
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import pandas as pd

class CodeMetricsDashboard:
    def __init__(self):
        self.metrics_file = ".windsurf/metrics/code_metrics.json"
        self.metrics: List[Dict[str, Any]] = []
        self._load_metrics()
    
    def _load_metrics(self):
        try:
            with open(self.metrics_file, 'r') as f:
                self.metrics = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.metrics = []
    
    def add_metric(self, metric_type: str, value: float, metadata: Dict[str, Any] = None):
        """Agrega una nueva métrica al dashboard."""
        metric = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": metric_type,
            "value": value,
            "metadata": metadata or {}
        }
        self.metrics.append(metric)
        self._save_metrics()
    
    def _save_metrics(self):
        """Guarda las métricas en el archivo JSON."""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def generate_report(self, days: int = 30):
        """Genera un informe de métricas para el período especificado."""
        df = pd.DataFrame(self.metrics)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filtrar por período
        cutoff = datetime.utcnow() - pd.Timedelta(days=days)
        recent_metrics = df[df['timestamp'] > cutoff]
        
        # Generar gráficos
        self._plot_metrics(recent_metrics)
        
        return recent_metrics.describe()
    
    def _plot_metrics(self, metrics_df):
        """Genera gráficos a partir de las métricas."""
        # Implementar generación de gráficos
        pass
```

## Implementación y Despliegue

1. **Configuración Inicial**:
   ```bash
   # Crear estructura de directorios
   mkdir -p .windsurf/{workflows,metrics,templates}
   mkdir -p scripts tests/{unit,integration} src
   
   # Inicializar entorno virtual
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   
   # Instalar dependencias
   pip install -r requirements.txt -r requirements-dev.txt
   ```

2. **Configuración de Secretos**:
   ```bash
   # Configurar secretos en GitHub
   gh secret set OPENAI_API_KEY --body="your-api-key"
   gh secret set SLACK_WEBHOOK --body="your-slack-webhook"
   ```

3. **Primera Ejecución**:
   ```bash
   # Ejecutar el workflow manualmente
   gh workflow run "Vibe Coding 24/7"
   ```

## Monitoreo y Mantenimiento

1. **Revisar Ejecuciones**:
   ```bash
   # Ver estado de los workflows
   gh run list --workflow="Vibe Coding 24/7"
   
   # Ver logs de una ejecución específica
   gh run view <run-id> --log
   ```

2. **Actualizar Dependencias**:
   ```bash
   # Actualizar dependencias de Python
   pip list --outdated
   pip install --upgrade -r requirements.txt
   pip freeze > requirements.txt
   ```

3. **Optimización Continua**:
   - Revisar métricas semanalmente
   - Ajustar prompts según resultados
   - Actualizar plantillas según necesidades del proyecto

## Recursos Adicionales

- [Guía de Estilo de Código](.windsurf/CODING_STANDARDS.md)
- [Documentación de la API](docs/api.md)
- [Proceso de Revisión de Código](.github/CODE_REVIEW.md)
- [Política de Ramas](.github/BRANCH_POLICY.md)