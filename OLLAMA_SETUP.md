# Configuración de Ollama para VibeFactory

Esta guía te ayudará a configurar Ollama para usar con VibeFactory.

## Pasos de instalación

1. **Instalar Ollama**
   - Descarga e instala Ollama desde [ollama.ai](https://ollama.ai/)
   - Sigue las instrucciones de instalación para tu sistema operativo

2. **Descargar un modelo**
   Abre una terminal y ejecuta uno de los siguientes comandos para descargar un modelo:
   ```bash
   # Para el modelo Llama 3 (recomendado)
   ollama pull llama3
   
   # O para Mistral
   ollama pull mistral
   
   # O para CodeLlama (mejor para generación de código)
   ollama pull codellama
   ```

3. **Iniciar el servidor de Ollama**
   El servidor de Ollama debería iniciarse automáticamente después de la instalación. Si necesitas reiniciarlo:
   ```bash
   # En Windows
   ollama serve
   
   # En macOS/Linux
   systemctl --user start ollama
   ```

4. **Verificar la instalación**
   ```bash
   ollama list
   ```
   Deberías ver una lista de los modelos que has descargado.

## Uso con VibeFactory

1. Asegúrate de que el servidor de Ollama esté en ejecución
2. Inicia VibeFactory normalmente
3. En la barra lateral, selecciona el modelo de Ollama que deseas usar
4. Comienza a usar la aplicación como de costumbre

## Solución de problemas

- **Error de conexión**: Asegúrate de que el servidor de Ollama esté en ejecución
  ```bash
  # Verificar estado del servicio
  ollama list
  ```

- **Modelo no encontrado**: Asegúrate de haber descargado el modelo
  ```bash
  # Listar modelos disponibles
  ollama list
  
  # Si no está listado, descárgalo
  ollama pull nombre-del-modelo
  ```

- **Rendimiento lento**: Los modelos más grandes pueden requerir más recursos
  - Prueba con un modelo más pequeño
  - Asegúrate de tener suficiente RAM disponible

## Modelos recomendados

- **llama3**: Buen equilibrio entre rendimiento y calidad
- **codellama**: Optimizado para generación de código
- **mistral**: Modelo más pequeño y rápido, buena calidad general

## Personalización avanzada

Puedes modificar los parámetros del modelo en el archivo `agents.py`:

```python
def __init__(self, model_name: str = "llama3"):
    self.model = Ollama(
        model=model_name,
        temperature=0.3,  # Controla la creatividad (0.0 a 1.0)
        num_ctx=4096,     # Tamaño del contexto
        num_predict=2048,  # Máximo de tokens a predecir
        top_p=0.9,        # Controla la diversidad
        top_k=40          # Limita las opciones de predicción
    )
```

## Notas adicionales

- Los modelos se descargan en `~/.ollama/models` por defecto
- El primer uso de un modelo puede tardar unos segundos mientras se carga en memoria
- Para detener el servidor de Ollama: `pkill -f ollama` (Linux/macOS) o cierra la ventana del terminal (Windows)
