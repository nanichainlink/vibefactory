# 🏭 VibeFactory

VibeFactory es una plataforma de desarrollo de software impulsada por IA que te permite generar aplicaciones completas a partir de una descripción en lenguaje natural. Con una interfaz intuitiva y potentes agentes de IA, podrás transformar tus ideas en código funcional en cuestión de minutos.

## 🚀 Características

- **Planificación Automática**: Descompone los requisitos en tareas técnicas accionables.
- **Generación de Código**: Código limpio y documentado generado automáticamente.
- **Interfaz Web Intuitiva**: Fácil de usar con Streamlit.
- **Arquitectura Modular**: Fácil de extender y personalizar.
- **Soporte para Múltiples Proyectos**: Desde aplicaciones web hasta APIs y scripts.

## 🛠️ Requisitos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Una clave de API de Perplexity (obtén una en [Perplexity AI](https://www.perplexity.ai/))

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/vibefactory.git
   cd vibefactory
   ```

2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   Crea un archivo `.env` en la raíz del proyecto con tu clave de API:
   ```
   PERPLEXITY_API_KEY=tu_clave_aqui
   ```

## 🚀 Uso

1. Inicia la aplicación:
   ```bash
   streamlit run app.py
   ```

2. Abre tu navegador en `http://localhost:8501`

3. Configura tu clave de API de Perplexity en la barra lateral

4. Ingresa la descripción de tu proyecto en el área principal

5. Haz clic en "Generar MVP" y observa cómo VibeFactory crea tu aplicación paso a paso

## 🏗️ Estructura del Proyecto

```
vibefactory/
├── app.py                # Aplicación principal de Streamlit
├── agents.py             # Agentes IA (Planificador y Generador de Código)
├── utils.py              # Utilidades y manejo de contexto
├── requirements.txt      # Dependencias del proyecto
├── .env.example         # Ejemplo de archivo de configuración
└── projects/             # Proyectos generados (se crea automáticamente)
```

## 🤖 Agentes

### Planificador
Analiza la descripción del proyecto y la descompone en tareas técnicas específicas.

### Generador de Código
Genera código Python limpio y documentado para cada tarea definida por el Planificador.

## 🌟 Ejemplo de Uso

1. **Descripción del Proyecto**:
   ```
   "Quiero una aplicación web para aprender SQL con juegos interactivos y desafíos"
   ```

2. **Tareas Generadas (ejemplo)**:
   1. Configurar proyecto básico con FastAPI y SQLAlchemy
   2. Crear modelos de base de datos para usuarios y puntuaciones
   3. Implementar autenticación de usuarios
   4. Crear interfaz de juego con Streamlit
   5. Implementar sistema de desafíos y recompensas

3. **Código Generado**:
   - Estructura de carpetas completa
   - Código fuente de la aplicación
   - Plantillas HTML/CSS
   - Scripts de base de datos

## 📊 Dashboard

La aplicación incluye un panel de control en tiempo real que muestra:
- Proyectos activos
- Estado de los agentes
- Tiempo promedio de generación
- Tasa de éxito

## 🛠️ Personalización

Puedes personalizar los agentes modificando los archivos:
- `agents.py`: Para ajustar la lógica de los agentes
- `utils.py`: Para modificar la gestión de proyectos
- `app.py`: Para personalizar la interfaz de usuario

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, lee nuestras [pautas de contribución](CONTRIBUTING.md) para más detalles.

## 📧 Contacto

¿Preguntas o sugerencias? ¡Nos encantaría saber de ti!
- Email: contacto@ejemplo.com
- Twitter: [@vibefactory](https://twitter.com/vibefactory)

---

Hecho con ❤️ por el equipo de VibeFactory
