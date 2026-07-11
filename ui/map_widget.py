from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class map_general(QWebEngineView):
    def __init__(self, lat=55.355198, lon=86.086847, zoom=15):
        super().__init__()

        self.lat = lat
        self.lon = lon
        self.zoom = zoom

        self._load_map()

    def _load_map(self):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <link rel="stylesheet"
                  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>

            <style>
                html, body, #map {{
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>

        <body>
            <div id="map"></div>

            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

            <script>
                var map = L.map('map').setView([{self.lat}, {self.lon}], {self.zoom});

                L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    maxZoom: 19,
                    attribution: 'OpenStreetMap contributors'
                }}).addTo(map);

                L.marker([{self.lat}, {self.lon}]).addTo(map)
                    .bindPopup("Вы здесь")
                    .openPopup();

                setTimeout(function() {{
                    map.invalidateSize();
                }}, 300);
            </script>
        </body>
        </html>
        """

        self.setHtml(html_content, QUrl("https://tile.openstreetmap.org/"))
