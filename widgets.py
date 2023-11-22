from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from urllib.request import urlopen

import apidb
import track_element
import album_element


def set_cover(url, picture):
    data = urlopen(url).read()
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    pixmap = pixmap.scaled(picture.minimumWidth(), picture.minimumHeight(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    picture.setPixmap(pixmap)


def shorten_long_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length - 1] + '...'
    return text


class TrackElement(QWidget, track_element.Ui_Form):
    def __init__(self, parent, data):
        super().__init__(parent)

        self.parent_class = parent
        self.preview_url = data['preview_url'] if 'preview_url' in data else ''
        self.track_id = data['uri'].split(':')[-1]

        self.setupUi(self)
        self.set_data(data)

    def set_data(self, data):
        self.name.setText(data['name'])
        self.artist.setText(data['artist'])

        self.duration.setText(data['duration'])

        set_cover(data['cover'], self.picture)
        self.button.clicked.connect(lambda x: self.click(data['uri']))
        self.playButton.clicked.connect(self.play_button)

    def click(self, uri):
        print(self.preview_url)
        data = apidb.get_similar_tracks(uri)

        self.parent_class.update_list(data)

    def pause_icon(self):
        self.playButton.setStyleSheet(self.playButton.styleSheet().replace('play_icon.png', 'pause_icon.png'))

    def play_icon(self):
        self.playButton.setStyleSheet(self.playButton.styleSheet().replace('pause_icon.png', 'play_icon.png'))

    def play_button(self):
        self.pause_icon()
        if not self.preview_url:
            self.preview_url = apidb.get_track_by_track_id(self.track_id)['preview_url']
            print(self.preview_url)
        self.play_preview()

    def play_preview(self):
        print('playing preview')
        self.parent_class.audio_manager.play_audio(self.preview_url, self)


class AlbumElement(QWidget, album_element.Ui_Form):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.parent_class = parent
        self.setupUi(self)
        self.set_data(data)

    def set_data(self, data):
        self.name.setText(shorten_long_text(data['name'], 18))
        self.artist.setText(shorten_long_text(data['artist'], 24))

        set_cover(data['cover'], self.picture)
        self.button.clicked.connect(lambda x: self.click(data['uri']))

    def click(self, uri):
        print(f'{uri}')
        data = apidb.get_similar_tracks(uri)

        self.parent_class.update_list(data)