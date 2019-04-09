import math
import os
import os.path
import Song
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen import File
from PyQt5 import QtGui


class SongDatabase:

    total = 0   # total songs

    @staticmethod
    def retrieve_songs(directory):
        my_songs = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in [f for f in filenames if f.endswith(".mp3")]:
                song_path = os.path.join(dirpath, filename)
                SongDatabase.get_song_info(path=song_path, my_songs=my_songs)
                SongDatabase.total += 1
                # print(os.path.join(dirpath, filename))

        print(SongDatabase.total, "songs found")
        SongDatabase.total = 0
        print(my_songs)
        return my_songs

    @staticmethod
    def get_song_info(path, my_songs):
        audio = EasyID3(path)
        audiom = MP3(path)
        pixmap = QtGui.QPixmap()
        metadata = File(path)

        length = round(audiom.info.length)
        seconds = (length % 60)/100         # mod to return seconds, divide by hundred formatting {min.sec}
        minutes = math.floor(length / 60)   # flooring since seconds taken care of above
        song_length = seconds + minutes

        for tag in metadata.tags.values():
            if tag.FrameID == 'APIC':
                pixmap.loadFromData(tag.data)
                print("HERE (SongDatabase.get_song_info)")
                break

        # It should be possible to do the following in one line each
        title = str(audio['title']).strip('[]')
        title = title.strip('"\'')
        artist = str(audio['artist']).strip('[]')
        artist = artist.strip('"\'')
        album = str(audio['album']).strip('[]')
        album = album.strip('"\'')

        my_songs.append(Song.Song(path, title, artist, album, song_length, pixmap))

    @staticmethod
    def print_song_info(my_songs):
        print("Printing ", len(my_songs))

        try:
            for i in range(len(my_songs)):
                print(my_songs[i].get_title(), " ", my_songs[i].get_artist(), " ", my_songs[i].get_album(), " ",
                      my_songs[i].get_length(), my_songs[i].get_path())

            return len(my_songs)

        except TypeError:
            pass

    @staticmethod
    def find_song_to_play(my_songs, search_song):
        print("Searching for: ", search_song)
        for i in range(len(my_songs)):
            if search_song == my_songs[i].get_title():
                print("Song found: ", my_songs[i].get_title())
                return

    @staticmethod
    def filter_songs_search(my_songs, search_filter):
        """Function to search for song title, album or artist."""
        instances_found = 0
        print("Searching for: ", search_filter)
        for i in range(len(my_songs)):
            if search_filter == my_songs[i].get_title():
                print("Song found: ", my_songs[i].get_title(), "Found: ", (instances_found+1), "row: ", i+1)
                instances_found += 1
            elif search_filter == my_songs[i].get_artist():
                print("Artist found: ", my_songs[i].get_title(), "Found: ", (instances_found + 1), "row: ", i + 1)
                instances_found += 1
            elif search_filter == my_songs[i].get_album():
                print("Album found: ", my_songs[i].get_album(), "Found: ", (instances_found + 1), "row: ", i + 1)
                instances_found += 1

        if instances_found == 0:
            print("Sorry, no songs found with the following Title or Artist or Album: ", search_filter)

