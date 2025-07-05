import folium
import json

class GPSLogic:
    """
    Maneja la lógica de negocio para la aplicación GPS.
    """
    def __init__(self, markers_file="markers.json"):
        self.markers_file = markers_file
        self.markers = self._load_markers()

    def _load_markers(self):
        """Carga los marcadores desde un archivo JSON."""
        try:
            with open(self.markers_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_markers(self):
        """Guarda los marcadores en un archivo JSON."""
        with open(self.markers_file, 'w') as f:
            json.dump(self.markers, f, indent=4)

    def add_marker(self, name: str, latitude: float, longitude: float, description: str = ""):
        """Añade un nuevo marcador a la lista."""
        self.markers.append({
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "description": description
        })
        self._save_markers()

    def get_markers(self):
        """Devuelve la lista de marcadores."""
        return self.markers

    def get_current_location(self):
        """
        Intenta obtener la ubicación actual del usuario.
        NOTA: Esto no es posible directamente desde el backend en Streamlit.
        Se devuelve None para que la app use una ubicación por defecto.
        """
        return None

    def create_map(self, center: tuple[float, float], zoom_start=13):
        """Crea un mapa de Folium con los marcadores actuales."""
        m = folium.Map(location=center, zoom_start=zoom_start)

        for marker in self.markers:
            folium.Marker(
                location=[marker['latitude'], marker['longitude']],
                popup=f"<b>{marker['name']}</b><br>{marker['description']}",
                tooltip=marker['name']
            ).add_to(m)
        
        # Añadir control de clics para obtener coordenadas
        m.add_child(folium.LatLngPopup())

        return m
