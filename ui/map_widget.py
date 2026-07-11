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
            <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
            <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet"/>
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
            <script>
                var map = new maplibregl.Map({{
                    container: 'map',
                    style: {{
                        version: 8,
                        sources: {{
                            osm: {{
                                type: 'raster',
                                tiles: ['https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png'],
                                tileSize: 256,
                                attribution: '&copy; OpenStreetMap contributors'
                            }}
                        }},
                        layers: [
                            {{
                                id: 'osm-layer',
                                type: 'raster',
                                source: 'osm',
                                minzoom: 0,
                                maxzoom: 19
                            }}
                        ]
                    }},
                    center: [{self.lon}, {self.lat}],
                    zoom: {self.zoom}
                }});

                map.addControl(new maplibregl.NavigationControl());

                new maplibregl.Marker()
                    .setLngLat([{self.lon}, {self.lat}])
                    .setPopup(new maplibregl.Popup().setHTML("Вы здесь"))
                    .addTo(map)
                    .togglePopup();

                map.on('load', function() {{
                    map.resize();
                }});
            </script>
        </body>
        </html>
        """
        self.setHtml(html_content, QUrl("https://tile.openstreetmap.org/"))