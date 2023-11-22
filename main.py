import sys
from PyQt5 import uic
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

import apidb
from audio_manager import AudioManager
from widgets import TrackElement, AlbumElement


# class TrackElement(QWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # uic.loadUi("track_element.ui", self)
#         uic.loadUi("untitled.ui", self)


class SongApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui.ui", self)

        QFontDatabase.addApplicationFont('futura/unicode.futurab.ttf')
        QFontDatabase.addApplicationFont('futura/futura light bt.ttf')

        self.search_bar_text = ''
        self.search_bar.editingFinished.connect(self.search, Qt.QueuedConnection)

        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.scroll_area_setup()

        self.audio_manager = AudioManager()

    def scroll_area_setup(self):
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)

        self.widget.setLayout(self.vbox)

    def search(self):
        if self.search_bar.text() == self.search_bar_text:
            return
        self.search_bar_text = self.search_bar.text()

        data = apidb.search(self.search_bar.text())

        self.update_list(data)

    def create_list_of_data(self, data, layout):
        if 'track' in data:
            self.create_tracks(data, layout)

        if 'album' in data:
            self.create_albums(data, layout)

    def update_list(self, data):
        self.clear_scroll_area()
        self.audio_manager.current_track = None
        self.create_list_of_data(data, self.vbox)

    def clear_scroll_area(self):
        self.clear_layout(self.vbox)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget()
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().deleteLater()
            else:
                self.clear_layout(layout.itemAt(i).layout())
                layout.itemAt(i).layout().deleteLater()

    def create_tracks(self, data, layout):
        for track in data['track']:
            print(track['name'])
            widget = TrackElement(self, track)

            layout.addWidget(widget)

    def create_albums(self, data, layout):
        row_length = 4
        for i in range(len(data['album']) // row_length):
            row = QHBoxLayout()

            for j in range(i * row_length, i * row_length + 4):
                album = data['album'][j]
                print(album['name'])

                widget = AlbumElement(self, album)

                row.addWidget(widget)

            layout.addLayout(row)

    def closeEvent(self, event):
        self.audio_manager.stop_audio()
        super().closeEvent(event)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SongApp()
    ex.show()
    print('123')
    sys.exit(app.exec())
