
import webbrowser as web
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices
from PySide6.QtCore import QTimer, Qt, QUrl

def open_git():
    url = "https://github.com/"
    web.open(url)

def open_doc():
    QDesktopServices.openUrl(
        QUrl.fromLocalFile("resources/doc.pdf")
    )
