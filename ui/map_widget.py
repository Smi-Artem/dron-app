

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl



class map_general(QWebEngineView):

    def __init__(self):
        super().__init__()

        self.setHtml("""
        <html>
        <body style="background-color:yellow;">
        <h1> КАРТА </h1>
        </body>
        </html>
        
        """)

        # self.setHtml("""
        # <!DOCTYPE html>
        # <html>
        # <head>
        # <link rel = "stylesheet"
        # href = "https://unpkg.com/leaflet/dist/leaflet.css"/>
        # <script src = "https://unpkg.com/leaflet/dist/leaflet.js">
        # </script>
        #
        # <style>
        #
        # html, body, #map{
        #     height: 100%;
        #     margin: 0;
        # }
        #
        # </style>
        # </head>
        #
        # <body>
        # <div id="map"></div>
        #
        # <script>
        #
        # let lat = 55.756;
        # let lon = 37.618;
        #
        # let map = L.map("map").setView([lat, lon], 15);
        # L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png")}",
        # {maxZoom: 19}).addTo(map);
        #
        # let marker = L.circleMarker(
        # [lat, lon],
        # {radius: 10,
        # color = "red",
        # fillColor = "red",
        # fillOpacity = 1,
        # }
        # ).addTo(map);
        #
        # function updateDrone(lat, lon)
        # {
        #     map.setView(
        #     [lat, lon],
        #     15);
        #
        #     marker.setLatLng([lat, lon]);
        # }
        #
        # </script>
        # </body>
        # </html>
        #
        # """)