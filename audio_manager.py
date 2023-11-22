import urllib.request
import time

from pygame import mixer
import os
import threading


class AudioManager:
    def __init__(self):
        mixer.init()
        self.set_volume(50)
        self.current_track = None
        self.pause_thread = None

    def play_audio(self, url, track):
        if self.current_track:
            self.current_track.play_icon()
            if track.track_id == self.current_track.track_id:
                self.stop_audio()
                self.current_track = None
                return

        self.stop_audio()
        self.download_track(url, track.track_id)

        mixer.music.load(f"music/{track.track_id}.mp3")
        mixer.music.play()
        self.current_track = track

        self.pause_thread = threading.Thread(target=self.wait_then_pause)
        self.pause_thread.start()

    def set_volume(self, volume):
        mixer.music.set_volume(volume / 100)

    def wait_then_pause(self):
        while mixer.music.get_busy():
            time.sleep(0.1)
        if self.current_track:
            self.current_track.play_icon()

    def download_track(self, url, track_id):
        if os.path.exists(f'music/{track_id}.mp3'):
            return
        urllib.request.urlretrieve(url, f'music/{track_id}.mp3')

    def stop_audio(self):
        mixer.music.stop()
