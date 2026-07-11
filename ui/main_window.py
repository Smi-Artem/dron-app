
from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QProgressBar, QWidget, QTabWidget,
    QPlainTextEdit, QFrame,
    QTextBrowser, QSplitter,
    QTableWidget, QTableWidgetItem,
    QAbstractItemView, QSizePolicy


)
from PySide6.QtGui import QFont
from PySide6.QtCore import QTimer, QDateTime, Qt, QSize
import core.serial_meneger as ser_meneger
import fitz
import os
from ui.map_widget import map_general


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.start_time = QDateTime.currentDateTime()
        self.disconnect_counter = 0
        self.center = QWidget()
        self.main_layout = QVBoxLayout(self.center)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.top_panel = self.create_top_panel()
        self.main_layout.addWidget(self.top_panel)
        self.tabs = QTabWidget()
        self.general = self.create_general_tab()
        self.mission = self.create_mission_tab()
        self.data = self.create_data_tab()
        self.recording = QWidget()

        self.tabs.addTab(self.general, "ОБЩЕЕ")
        self.tabs.addTab(self.mission, "МИССИЯ")
        self.tabs.addTab(self.data, "ДАННЫЕ")
        self.tabs.addTab(self.recording, "ТРАНСЛЯЦИЯ (BETA)")
        self.main_layout.addWidget(self.tabs, stretch=1)
        self.create_console()
        self.setCentralWidget(self.center)
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_ui_loop)
        self.ui_timer.start(1000)
        ser_meneger.find_adr()

    def create_top_panel(self):
        panel_widget = QWidget()
        layout = QHBoxLayout(panel_widget)
        layout.setContentsMargins(15, 5, 15, 5)
        layout.setSpacing(20)

        # Темный фон для панели
        panel_widget.setStyleSheet("background-color: #333; color: white; font-size: 14px;")

        self.lbl_status = QLabel("WAITING")
        self.lbl_status.setStyleSheet("color: #cc9900; font-weight: bold;")

        self.lbl_port = QLabel("COM?")
        self.lbl_battery = QLabel("0%")  # добавить логику батареи позже
        self.lbl_time = QLabel("00:00:00")


        sep1 = QFrame()
        sep1.setFrameShape(QFrame.VLine)
        sep1.setFixedWidth(1)
        sep1.setStyleSheet("color: #555;")
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.VLine)
        sep2.setFixedWidth(1)
        sep2.setStyleSheet("color: #555;")

        layout.addStretch()
        layout.addWidget(self.lbl_status)
        layout.addWidget(sep1)
        layout.addWidget(self.lbl_port)
        layout.addWidget(sep2)
        layout.addWidget(self.lbl_battery)
        layout.addWidget(self.lbl_time)

        return panel_widget

    def create_console(self):
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.appendPlainText("System Initialized...")
        self.console.appendPlainText("Waiting for connection...")

        self.console.setMaximumHeight(250)
        self.console.setMinimumHeight(250)
        self.main_layout.addWidget(self.console)


    def update_ui_loop(self):

        now = QDateTime.currentDateTime()
        start = self.start_time
        elapsed_secs = now.toSecsSinceEpoch() - start.toSecsSinceEpoch()
        if elapsed_secs < 0:
            elapsed_secs = 0
        hours, remainder = divmod(elapsed_secs, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.lbl_time.setText(time_str)
        is_connected, port_name = ser_meneger.check_connection()

        if is_connected and port_name:
            self.lbl_port.setText(str(port_name))
            self.lbl_status.setText("CONNECTED")
            self.lbl_status.setStyleSheet("color: green; font-weight: bold;")
            self.disconnect_counter = 0
        else:
            self.lbl_port.setText("NONE")
            self.lbl_status.setText("DISCONNECTED")
            self.lbl_status.setStyleSheet("color: red; font-weight: bold;")

            self.disconnect_counter += 1
            if self.disconnect_counter >= 3:
                self.console.appendPlainText("[WARNING] Dock station disconnected! Check connection.")
                self.disconnect_counter = 0

    def load_news_pdf(self):

        path_news = "resources/news.pdf"

        if not os.path.exists(path_news):
            self.news_browser.setText("Новости отсутствуют")
            return

        try:

            doc = fitz.open(path_news)
            html = ""

            color_rules = {
                "Последнее обновл": "yellow",
                "Чтобы узнавать об изменениях": "orange",
                "По предложениям, вопросам и информации об ошибках обращайтесь на почту": "pink",
                "Важно": "red",
                "Добавлено": "green",
                "Исправлено": "green",
                "https://": "blue",
                "@": "blue",


            }

            for page_ind in range(len(doc)):
                page = doc[page_ind]
                text = page.get_text()
                for line in text.split("\n"):
                    color = "white"
                    for word, clr in  color_rules.items():
                        if word in line:
                            color = clr
                            break
                    if "#" not in line:
                        html += (f"""
                        <span style="color: {color};">
                        {line}
                        </span><br>
                        """)
                    else:
                        continue

            self.news_browser.setHtml(html)
            doc.close()
        except Exception as e:
            self.news_browser.setText(f"{e}")

    def create_general_tab(self):

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        news_frame = QFrame()
        news_frame.setFixedWidth(350)
        news_layout = QVBoxLayout(news_frame)
        title = QLabel("NEWS")
        title.setStyleSheet('''
        font-size: 18px;
        font-weight: bold;
        ''')
        self.news_browser = QTextBrowser()
        news_layout.addWidget(title)
        news_layout.addWidget(self.news_browser)
        info = QFrame()
        self.map_general = map_general()
        self.map_general.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.map_general.setMinimumSize(500, 400)
        layout.addWidget(news_frame)
        layout.addWidget(self.map_general, stretch=1)
        self.load_news_pdf()

        return widget





    def create_mission_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        btn_start = QPushButton("СТАРТ МИССИИ")
        btn_start.setFont(QFont("Arial", 24, QFont.Bold))
        btn_start.setStyleSheet("""
              QPushButton {
                  background-color: #2ecc71;
                  color: white;
                  border: none;
                  padding: 20px 40px;
                  border-radius: 10px;
              }
              QPushButton:hover { background-color: #27ae60; }
              QPushButton:pressed { background-color: #1e8449; }
          """)
        btn_start.setMinimumSize(QSize(300, 100))

        btn_start.clicked.connect(self.on_start_mission_clicked)

        layout.addWidget(btn_start)
        return widget

    def on_start_mission_clicked(self):
        data_to_send = "START"
        success = ser_meneger.send_pack(data_to_send)
        if success:
            self.console.appendPlainText(f"[INFO] Sent command: {data_to_send}")
        else:
            self.console.appendPlainText("[ERROR] Failed to send command. Check connection.")

    def create_data_tab(self):

        widget = QWidget()
        layout = QHBoxLayout(widget)
        splitter = QSplitter(Qt.Horizontal)
        self.table = QTableWidget()
        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            [
                "№",
                "Объект",
                "Координаты",
                "Фото"
            ]
        )

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.photo = QLabel("Фото не выбрано") ###
        self.photo.setAlignment(Qt.AlignCenter)
        self.photo.setStyleSheet("""
            border:2px solid gray;
            font-size:18px;
        """)
        splitter.addWidget(self.table)
        splitter.addWidget(self.photo)
        splitter.setSizes([700, 500])
        layout.addWidget(splitter)

        ### временная передача данных

        self.add_detection(
            "Человек",
            "55.7561, 37.6182"
        )

        self.add_detection(
            "Рюкзак",
            "55.7568, 37.6200"
        )

        self.add_detection(
            "Автомобиль",
            "55.7572, 37.6210"
        )

        return widget

    def create_recording_tab(self):
        pass

    def add_detection(self, name, coords):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(
            row,
            0,
            QTableWidgetItem(str(row + 1))
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(name)
        )
        self.table.setItem(
            row,
            2,
            QTableWidgetItem(coords)
        )
        button = QPushButton("Открыть")
        button.clicked.connect(
            lambda _, r=row: self.open_photo(r)
        )
        self.table.setCellWidget(
            row,
            3,
            button
        )

    def open_photo(self, row):

        self.photo.setText(

            f"""Фотография

    Запись №{row + 1}

    Пока отсутствует"""

        )

















