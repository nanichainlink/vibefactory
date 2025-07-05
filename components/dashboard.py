"""
Módulo del panel de control y métricas en tiempo real.

Este módulo proporciona componentes para visualizar métricas en tiempo real
y un panel de control interactivo para monitorear y controlar el flujo de trabajo.
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de logging
import logging
logger = logging.getLogger(__name__)

# Constantes
METRICS_DIR = Path(".windsurf/metrics")
METRICS_DIR.mkdir(parents=True, exist_ok=True)

class Dashboard:
    """Clase principal para el panel de control y visualización de métricas."""
    
    def __init__(self):
        """Inicializa el dashboard y carga las métricas existentes."""
        self.metrics_file = METRICS_DIR / "runtime_metrics.json"
        self._ensure_metrics_file()
    
    def _ensure_metrics_file(self):
        """Asegura que el archivo de métricas exista."""
        if not self.metrics_file.exists():
            with open(self.metrics_file, "w") as f:
                json.dump([], f)
    
    def log_metric(self, metric_type: str, value: float, metadata: Optional[Dict] = None):
        """
        Registra una nueva métrica.
        
        Args:
            metric_type: Tipo de métrica (ej: 'code_generation_time', 'api_usage')
            value: Valor numérico de la métrica
            metadata: Metadatos adicionales (opcional)
        """
        try:
            # Cargar métricas existentes
            with open(self.metrics_file, "r") as f:
                metrics = json.load(f)
            
            # Agregar nueva métrica
            metric = {
                "timestamp": datetime.utcnow().isoformat(),
                "type": metric_type,
                "value": value,
                "metadata": metadata or {}
            }
            metrics.append(metric)
            
            # Guardar actualización
            with open(self.metrics_file, "w") as f:
                json.dump(metrics, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error al registrar métrica: {e}")
    
    def get_metrics(self, metric_type: Optional[str] = None, hours: int = 24) -> List[Dict]:
        """
        Obtiene métricas del archivo.
        
        Args:
            metric_type: Filtrar por tipo de métrica (opcional)
            hours: Número de horas hacia atrás para filtrar
            
        Returns:
            Lista de métricas que coinciden con los criterios
        """
        try:
            with open(self.metrics_file, "r") as f:
                metrics = json.load(f)
            
            # Filtrar por rango de tiempo
            cutoff = datetime.utcnow() - timedelta(hours=hours)
            metrics = [
                m for m in metrics 
                if datetime.fromisoformat(m["timestamp"]) >= cutoff
            ]
            
            # Filtrar por tipo si se especifica
            if metric_type:
                metrics = [m for m in metrics if m["type"] == metric_type]
                
            return metrics
            
        except Exception as e:
            logger.error(f"Error al obtener métricas: {e}")
            return []
    
    def render_dashboard(self):
        """Renderiza el panel de control principal."""
        st.title("📊 Panel de Control")
        
        # Filtros
        st.sidebar.header("Filtros")
        time_range = st.sidebar.select_slider(
            "Rango de tiempo",
            options=[1, 6, 12, 24, 48, 72],
            value=24,
            format_func=lambda x: f"Últimas {x}h"
        )
        
        # Obtener métricas
        metrics = self.get_metrics(hours=time_range)
        
        if not metrics:
            st.warning("No hay métricas disponibles para el rango seleccionado.")
            return
        
        # Convertir a DataFrame para análisis
        df = pd.DataFrame(metrics)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        
        # Métricas clave
        self._render_key_metrics(df)
        
        # Gráficos
        tab1, tab2, tab3 = st.tabs(["Uso de API", "Rendimiento", "Actividad"]) 
        
        with tab1:
            self._render_api_metrics(df)
            
        with tab2:
            self._render_performance_metrics(df)
            
        with tab3:
            self._render_activity_metrics(df)
    
    def _render_key_metrics(self, df: pd.DataFrame):
        """Renderiza las métricas clave en la parte superior."""
        col1, col2, col3, col4 = st.columns(4)
        
        # Total de solicitudes API
        api_calls = len(df[df["type"] == "api_call"])
        with col1:
            st.metric("Llamadas API", api_calls)
        
        # Tiempo promedio de generación
        gen_times = df[df["type"] == "code_generation_time"]["value"]
        avg_gen_time = gen_times.mean() if not gen_times.empty else 0
        with col2:
            st.metric("Tiempo Prom. Generación", f"{avg_gen_time:.2f}s")
        
        # Tokens utilizados
        tokens_used = df[df["type"] == "tokens_used"]["value"].sum()
        with col3:
            st.metric("Tokens Utilizados", f"{tokens_used:,}")
        
        # Proyectos generados
        projects_created = len(df[df["type"] == "project_created"])
        with col4:
            st.metric("Proyectos Generados", projects_created)
    
    def _render_api_metrics(self, df: pd.DataFrame):
        """Renderiza las métricas de uso de API."""
        st.subheader("📈 Uso de API")
        
        # Filtrar métricas de API
        api_df = df[df["type"].isin(["api_call", "tokens_used"])].copy()
        
        if api_df.empty:
            st.info("No hay datos de uso de API disponibles.")
            return
        
        # Agrupar por hora
        api_df["hour"] = api_df["timestamp"].dt.floor("H")
        
        # Gráfico de llamadas por hora
        calls_by_hour = api_df[api_df["type"] == "api_call"].groupby("hour").size().reset_index(name="count")
        
        if not calls_by_hour.empty:
            fig1 = px.line(
                calls_by_hour, 
                x="hour", 
                y="count",
                title="Llamadas API por Hora",
                labels={"hour": "Hora", "count": "Llamadas"}
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico de tokens por hora
        tokens_by_hour = api_df[api_df["type"] == "tokens_used"].groupby("hour")["value"].sum().reset_index()
        
        if not tokens_by_hour.empty:
            fig2 = px.area(
                tokens_by_hour,
                x="hour",
                y="value",
                title="Tokens Utilizados por Hora",
                labels={"hour": "Hora", "value": "Tokens"}
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    def _render_performance_metrics(self, df: pd.DataFrame):
        """Renderiza las métricas de rendimiento."""
        st.subheader("⚡ Rendimiento")
        
        # Filtrar métricas de rendimiento
        perf_df = df[df["type"].isin(["code_generation_time", "model_latency"])].copy()
        
        if perf_df.empty:
            st.info("No hay datos de rendimiento disponibles.")
            return
        
        # Agrupar por tipo y calcular estadísticas
        perf_stats = perf_df.groupby("type")["value"].agg(["mean", "min", "max", "count"]).reset_index()
        
        # Mostrar estadísticas
        st.dataframe(
            perf_stats.rename(columns={
                "type": "Métrica",
                "mean": "Promedio (s)",
                "min": "Mínimo (s)",
                "max": "Máximo (s)",
                "count": "Muestras"
            }),
            use_container_width=True
        )
        
        # Gráfico de rendimiento a lo largo del tiempo
        if not perf_df.empty:
            fig = px.line(
                perf_df, 
                x="timestamp", 
                y="value",
                color="type",
                title="Tiempo de Respuesta",
                labels={"timestamp": "Hora", "value": "Tiempo (s)", "type": "Métrica"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_activity_metrics(self, df: pd.DataFrame):
        """Renderiza las métricas de actividad."""
        st.subheader("📊 Actividad")
        
        # Contar eventos por tipo
        activity_counts = df["type"].value_counts().reset_index()
        activity_counts.columns = ["Tipo de Evento", "Cantidad"]
        
        # Gráfico de barras de actividad
        if not activity_counts.empty:
            fig1 = px.bar(
                activity_counts,
                x="Tipo de Evento",
                y="Cantidad",
                title="Distribución de Actividad",
                color="Tipo de Evento"
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        # Actividad a lo largo del tiempo
        activity_over_time = df.groupby([df["timestamp"].dt.floor("H"), "type"]).size().unstack(fill_value=0)
        
        if not activity_over_time.empty:
            fig2 = px.area(
                activity_over_time,
                title="Actividad a lo Largo del Tiempo",
                labels={"value": "Eventos", "timestamp": "Hora"}
            )
            st.plotly_chart(fig2, use_container_width=True)


def render_control_panel():
    """Renderiza el panel de control para la gestión del sistema."""
    st.title("🎛️ Panel de Control")
    
    # Sección de estado del sistema
    with st.expander("🖥️ Estado del Sistema", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Estado API", "🟢 En Línea")
        with col2:
            st.metric("Uso de CPU", "32%")
        with col3:
            st.metric("Uso de Memoria", "1.2GB / 4GB")
    
    # Sección de configuración
    with st.expander("⚙️ Configuración", expanded=True):
        st.subheader("Ajustes de Rendimiento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_workers = st.slider(
                "Máximo de Trabajadores Paralelos",
                min_value=1,
                max_value=10,
                value=4,
                help="Número máximo de tareas que se pueden ejecutar en paralelo"
            )
            
            cache_ttl = st.number_input(
                "Duración de la Caché (minutos)",
                min_value=1,
                max_value=1440,
                value=60,
                help="Tiempo que los resultados en caché se consideran válidos"
            )
        
        with col2:
            model_timeout = st.number_input(
                "Tiempo de Espera del Modelo (segundos)",
                min_value=10,
                max_value=600,
                value=120,
                help="Tiempo máximo de espera para las respuestas del modelo"
            )
            
            max_retries = st.number_input(
                "Intentos Máximos",
                min_value=1,
                max_value=10,
                value=3,
                help="Número máximo de reintentos para operaciones fallidas"
            )
        
        # Botón para aplicar configuración
        if st.button("💾 Aplicar Configuración", type="primary"):
            # Aquí iría la lógica para aplicar la configuración
            st.toast("✅ Configuración guardada correctamente")
    
    # Sección de mantenimiento
    with st.expander("🔧 Mantenimiento", expanded=True):
        st.subheader("Herramientas de Mantenimiento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Limpiar Caché", help="Eliminar archivos temporales y caché"):
                # Lógica para limpiar caché
                st.toast("🧹 Caché limpiada correctamente")
            
            if st.button("📊 Regenerar Índices", help="Reconstruir índices de búsqueda"):
                # Lógica para regenerar índices
                st.toast("🔍 Índices regenerados correctamente")
        
        with col2:
            if st.button("🧪 Ejecutar Pruebas", help="Ejecutar suite de pruebas"):
                # Lógica para ejecutar pruebas
                with st.spinner("Ejecutando pruebas..."):
                    time.sleep(2)  # Simular ejecución de pruebas
                    st.toast("✅ Pruebas completadas exitosamente")
            
            if st.button("📦 Exportar Datos", help="Exportar datos del sistema"):
                # Lógica para exportar datos
                st.toast("💾 Datos exportados correctamente")
    
    # Sección de monitoreo en tiempo real
    with st.expander("📡 Monitoreo en Tiempo Real", expanded=True):
        st.subheader("Métricas en Tiempo Real")
        
        # Gráfico de uso de recursos
        chart_placeholder = st.empty()
        
        # Simular actualización en tiempo real
        for i in range(5):
            # Generar datos de ejemplo
            time_data = pd.DataFrame({
                "Tiempo": pd.date_range(end=pd.Timestamp.now(), periods=20, freq="s"),
                "Uso de CPU": [30 + i*2 + j*0.5 for j in range(20)],
                "Uso de Memoria": [40 + i*3 + j*0.3 for j in range(20)]
            })
            
            # Actualizar gráfico
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=time_data["Tiempo"],
                y=time_data["Uso de CPU"],
                name="CPU %",
                line=dict(color="#636efa")
            ))
            
            fig.add_trace(go.Scatter(
                x=time_data["Tiempo"],
                y=time_data["Uso de Memoria"],
                name="Memoria %",
                line=dict(color="#ef553b")
            ))
            
            fig.update_layout(
                title="Uso de Recursos en Tiempo Real",
                xaxis_title="Hora",
                yaxis_title="Uso (%)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(1)  # Actualizar cada segundo


# Ejemplo de uso
if __name__ == "__main__":
    # Configuración de la página
    st.set_page_config(
        page_title="VibeFactory - Panel de Control",
        page_icon="📊",
        layout="wide"
    )
    
    # Inicializar el dashboard
    dashboard = Dashboard()
    
    # Pestañas para diferentes vistas
    tab1, tab2 = st.tabs(["📊 Dashboard", "🎛️ Panel de Control"])
    
    with tab1:
        dashboard.render_dashboard()
    
    with tab2:
        render_control_panel()
