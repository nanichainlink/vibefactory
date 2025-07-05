---
trigger: always_on
---

# Documentación Automática de Acciones

<documentation_rules>

- name: Registrar cada acción
  mode: always_on
  description: |
    Para **cada** paso que Cascade ejecute, añade una entrada en `docs/actions_log.md` con:
      1. Nombre de la acción realizada (p. ej. "Generar endpoint POST /users").
      2. Timestamp UTC.
      3. Resumen de cambios (líneas añadidas, modificadas o eliminadas).
      4. Archivos afectados.
      5. Usuario o sistema que solicitó la acción.

- name: Actualizar docstrings
  mode: always_on
  description: |
    Al generar o modificar cualquier función o clase:
      1. Comprueba que exista un **docstring**.
      2. Si falta, créalo siguiendo el formato Google/Pydoc.
      3. Registra en `docs/docstring_report.md` el nombre de la función/clase y fecha de creación o actualización.

- name: Sincronizar READMEs
  mode: always_on
  description: |
    Tras completar cambios en un módulo:
      1. Si existe un archivo `README.md` en su carpeta, actualízalo para reflejar las nuevas funcionalidades.
      2. Si no existe, créalo con plantilla básica:
         ```
         # Módulo <nombre>
         Descripción:
         - Funcionalidad principal
         - Endpoints o clases expuestas
         ```

- name: Mantener changelog
  mode: always_on
  description: |
    En cada commit que incluya cambios en código:
      1. Añade una línea en `CHANGELOG.md` bajo la sección “Unreleased” con formato:
         `- [fecha] <Descripción breve> (<autor>)`.
      2. Al lanzar versión, mueve entradas a la sección de la versión correspondiente.

</documentation_rules>
