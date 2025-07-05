---
description: # Workflow 24/7 - Generación Continua Automatizada
---

# Workflow 24/7 - Generación Continua Automatizada

## Descripción
Flujo de trabajo automatizado para generación continua de código con IA, ejecutándose 24/7 con ciclos de 5 minutos.

## Configuración

```yaml
name: Generación Continua 24/7
on:
  schedule:
    - cron: '*/5 * * * *'  # Ejecutar cada 5 minutos
  workflow_dispatch:  # Permite ejecución manual

concurrency:
  group: "24-7-workflow"
  cancel-in-progress: true  # Cancela ejecuciones anteriores si aún están en curso

jobs:
  generate-code:
    name: Generar Código Automatizado
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout del código
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Ejecutar análisis de contexto
        run: python -m scripts.analyze_context

      - name: Generar código con IA
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python -m scripts.generate_code

      - name: Ejecutar pruebas unitarias
        run: |
          python -m pytest tests/unit -v

      - name: Ejecutar pruebas de integración
        run: |
          python -m pytest tests/integration -v

      - name: Validar calidad de código
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

      - name: Formatear código
        run: |
          black .
          isort .


      - name: Commit y Push de cambios
        if: success()
        run: |
          git config --local user.email "ia-assistant@conectatech.com"
          git config --local user.name "IA Assistant"
          git add .
          git diff-index --quiet HEAD || (git commit -m "[AUTO] Actualización automática de código" && git push origin main)

      - name: Notificar resultado
        if: always()
        uses: rtCamp/action-slack-notify@v2
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
          SLACK_COLOR: ${{ job.status == 'success' && 'good' || 'danger' }}
          SLACK_TITLE: "Ejecución del Workflow 24/7"
          SLACK_MESSAGE: "Estado: ${{ job.status }}\nDetalles: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

## Estructura de Carpetas Recomendada

```
.
├── .github/workflows/
│   └── 24_7_workflow.yml    # Configuración del workflow
├── scripts/
│   ├── __init__.py
│   ├── analyze_context.py    # Análisis de contexto
│   ├── generate_code.py      # Generación de código con IA
│   └── validate_code.py      # Validación de código
├── tests/
│   ├── unit/               # Pruebas unitarias
│   └── integration/         # Pruebas de integración
└── src/                     # Código fuente
```

## Variables de Entorno Requeridas

```env
# Configuración de la API de IA
OPENAI_API_KEY=tu_api_key_aqui

# Configuración de notificaciones
SLACK_WEBHOOK=https://hooks.slack.com/...


# Configuración del repositorio
GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
```

## Exclusión de Archivos

El workflow está configurado para ignorar automáticamente cambios en:
- Archivos de documentación (*.md, *.txt)
- Archivos de configuración local (.env, config.local.*)
- Archivos temporales y de IDE (__pycache__, .vscode, .idea)
- Archivos de entorno virtual (venv/, env/, .venv/)

## Monitoreo y Métricas

Se recomienda configurar:
1. Monitoreo de ejecuciones fallidas
2. Métricas de calidad de código
3. Tiempo promedio de generación
4. Tasa de éxito de pruebas
5. Cobertura de código

## Notas de Implementación

1. **Seguridad**: Nunca expongas las claves de API en el código. Usa GitHub Secrets.
2. **Rendimiento**: Ajusta la frecuencia según las necesidades del proyecto.
3. **Control de Calidad**: Mantén los estándares altos para las pruebas automáticas.
4. **Retroalimentación**: Revisa regularmente los logs y métricas para mejorar el proceso.
5. **Escalabilidad**: Considera ejecutores auto-hospedados para proyectos grandes.
