import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout

import apidb
from audio_manager import AudioManager


from windows import Settings, MainWindow
from widgets import TrackElement, AlbumElement


class SongApp(MainWindow):
    def __init__(self):
        super().__init__()

        self.audio_manager = AudioManager()
        self.settings = Settings(self.audio_manager)
        self.settingsButton.clicked.connect(self.settings_button)

        self.settings.darkButton.clicked.connect(lambda x: self.set_theme(True))
        self.settings.lightButton.clicked.connect(lambda x: self.set_theme(False))

        self.set_theme(False)

    def set_theme(self, is_dark):
        if is_dark:
            self.set_dark_theme(self)
            self.set_dark_theme(self.settings)
        else:
            self.set_light_theme(self)
            self.set_light_theme(self.settings)

    def search(self):
        if self.search_bar.text() == '' or self.search_bar.text() == self.search_bar_text:
            return
        self.search_bar_text = self.search_bar.text()

        data = apidb.search(self.search_bar.text())

        self.update_list(data)

    def create_list_of_data(self, data, layout):
        if 'track' in data:
            self.create_tracks(data, layout)

        if 'album' in data:
            self.create_albums(data, layout)

    def create_tracks(self, data, layout):
        print('creating tracks')
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

    def settings_button(self):
        self.settings.show()

    def update_list(self, data):
        self.clear_scroll_area()
        self.audio_manager.current_track = None
        self.create_list_of_data(data, self.vbox)

    def closeEvent(self, event):
        self.audio_manager.stop_audio()
        self.settings.close()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SongApp()
    ex.show()
    sys.exit(app.exec())
