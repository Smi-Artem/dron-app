import sys
from PySide6.QtWidgets import QApplication
from ui.load_window import LoadWindow


app = QApplication(sys.argv)

with open("style/style.qss", "r", encoding="utf-8") as stl:
    app.setStyleSheet(stl.read())

window = LoadWindow()
window.show()

sys.exit(app.exec()) #чтоб не закрывалось