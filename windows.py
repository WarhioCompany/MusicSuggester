from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

import settings
import main_window


class Settings(QMainWindow, settings.Ui_MainWindow):
    def __init__(self, audio_manager):
        super().__init__()
        self.setupUi(self)
        self.volumeSlider.valueChanged.connect(self.volume_control)
        self.currentVolume = 50
        self.audio_manager = audio_manager

    def volume_control(self):
        self.currentVolume = self.volumeSlider.value()
        self.volume.setText(f'Volume {self.currentVolume}%')
        self.audio_manager.set_volume(self.currentVolume)


class MainWindow(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        QFontDatabase.addApplicationFont('futura/unicode.futurab.ttf')
        QFontDatabase.addApplicationFont('futura/futura light bt.ttf')

        self.search_bar_text = ''
        self.search_bar.returnPressed.connect(self.search, Qt.QueuedConnection)

        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.scroll_area_setup()

        self.set_light_theme(self)

    def scroll_area_setup(self):
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)

        self.widget.setLayout(self.vbox)

    def clear_scroll_area(self):
        self.clear_layout(self.vbox)

    def set_light_theme(self, window):
        with open('lighttheme.stylesheet') as file:
            window.setStyleSheet(file.read())

    def set_dark_theme(self, window):
        with open('darktheme.stylesheet') as file:
            window.setStyleSheet(file.read())

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget()
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().deleteLater()
            else:
                self.clear_layout(layout.itemAt(i).layout())
                layout.itemAt(i).layout().deleteLater()
