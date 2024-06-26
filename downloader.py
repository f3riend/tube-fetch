import os
from pytube import YouTube, Playlist
from icecream import ic

class YtDownloader:

    def __init__(self):
        self.downloads = os.path.join("C:/Users", os.getlogin(), "Downloads")

    def change(self, file_name, new_extension):
        file_name, old_extension = os.path.splitext(file_name)
        new_file_name = file_name + new_extension
        try:
            os.rename(file_name + old_extension, new_file_name)
        except FileNotFoundError:
            ic("Specified file not found.")

    def mp4(self, link):
        YouTube(link).streams.get_highest_resolution().download(output_path=self.downloads)
        ic("downloaded")

    def mp3(self, link):
        filename = YouTube(link).streams.filter(only_audio=True).get_audio_only().download(output_path=self.downloads)
        self.change(filename, ".mp3")
        ic("downloaded")

    def pmp4(self, link):
        playlist = Playlist(link)
        for video in playlist.videos:
            video.streams.get_highest_resolution().download(output_path=self.downloads)
            ic(f"downloaded {video.title}")

    def pmp3(self, link):
        playlist = Playlist(link)
        for video in playlist.videos:
            filename = video.streams.filter(only_audio=True).get_audio_only().download(output_path=self.downloads)
            self.change(filename, ".mp3")
            ic(f"downloaded {video.title}")
