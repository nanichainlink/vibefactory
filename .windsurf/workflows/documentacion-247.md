---
description: # Documentación Automática de Acciones
---

# Documentación Automática de Acciones

- name: Registrar cada acción
  mode: always_on
  description: |
    Cada vez que Cascade ejecute un comando, añade en `docs/actions_log.md`:
      • Acción realizada  
      • Timestamp UTC  
      • Resumen de líneas añadidas/modificadas/eliminadas  
      • Archivos afectados  

- name: Actualizar docstrings
  mode: always_on
  description: |
    Al crear o modificar funciones/clases:
      • Verifica existencia de docstring.  
      • Si falta, créalo en formato Google/Pydoc.  
      • Registra cambios en `docs/docstring_report.md`.  

- name: Sincronizar READMEs
  mode: always_on
  description: |
    Tras cambios en un módulo:
      • Actualiza o crea `README.md` con descripción y endpoints/clases expuestas.  

- name: Mantener changelog
  mode: always_on
  description: |
    En cada commit:
      • Añade línea en `CHANGELOG.md` bajo “Unreleased”:  
        `- [YYYY-MM-DD] Descripción (autor)`  
