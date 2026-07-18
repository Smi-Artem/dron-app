from PySide6.QtGui import QIcon, QPixmap, QDesktopServices
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
    QWidget
)
from PySide6.QtCore import QTimer, Qt, QUrl
import core.serial_meneger as ser_meneger
from ui.main_window import MainWindow                   ####
import core.url_docs as dgs

class LoadWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.create_window()
        self.create_widgets()
        self.create_layout()
        self.create_connect()

    def create_window(self):

        self.setWindowTitle("Окно ожидания")
        self.setWindowIcon(QIcon('resources/logo.png'))
        self.setFixedSize(900, 600)

    def create_widgets(self):

        # Логотип
        ilustration = QPixmap("resources/logo.png")
        self.logo = QLabel()
        self.logo.setPixmap(ilustration)

        self.logo.setAlignment(Qt.AlignCenter) ### ???
        self.logo.setPixmap(
            ilustration.scaled(
                150,
                150,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )


        # Заголовок

        self.title = QLabel("SmArtSeeker")
        self.title.setAlignment(Qt.AlignCenter) ### ???
        self.title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        # status

        self.status = QLabel("Search usb-hub")
        self.status.setAlignment(Qt.AlignCenter)


        #progress bar

        self.progress = QProgressBar()
        self.progress.setObjectName("progressBar")
        self.progress.setRange(0, 0)

        #Кнопки

        self.support_button = QPushButton("AI-ПОДДЕРЖКА")
        self.github_button = QPushButton("GitHub")
        self.docs_button = QPushButton("ДОКУМЕНТАЦИЯ")

        self.support_button.setObjectName("support_button")
        self.github_button.setObjectName("github_button")
        self.docs_button.setObjectName("docs_button")

    # расположение элементов
    def create_layout(self):

        # main cont

        container = QWidget()
        self.setCentralWidget(container)

        # main layount

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20)

        # add elements

        main_layout.addWidget(self.logo)
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.status)
        main_layout.addWidget(self.progress)

        #layout for button

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.support_button)
        button_layout.addWidget(self.github_button)
        button_layout.addWidget(self.docs_button)


        # add it

        main_layout.addLayout(button_layout)
        container.setLayout(main_layout)

    #connect signal

    def create_connect(self):

        self.timer = QTimer()
        self.timer.timeout.connect(self.scan_ports) ###
        self.timer.start(1000) ###
        self.docs_button.clicked.connect(self.open_docs)
        self.github_button.clicked.connect(self.open_github)


    # find arduino
    def scan_ports(self):

        port = ser_meneger.find_adr()
        if port not in {None}:
            self.status.setText(f"connect:{port}")
            self.timer.stop()
            QTimer.singleShot(3000, self.open_main)


    def open_docs(self):
        dgs.open_doc()

    def open_github(self):
        dgs.open_git()


    def open_support(self):
        pass

    def open_main(self):


        self.main = MainWindow()
        self.main.show()
        self.close()





