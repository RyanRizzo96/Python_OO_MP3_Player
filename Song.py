class Song:
    def __init__(self, path, title, artist, album, length, art):

        self.path = path
        self.title = title
        self.album = album
        self.artist = artist
        self.length = length
        self.art = art

    def get_path(self):
        return self.path

    def get_title(self):
        return self.title

    def set_title(self, new_title):
        self.title = new_title

    def get_album(self):
        return self.album

    def set_album(self, new_album):
        self.album = new_album

    def get_artist(self):
        return self.artist

    def set_artist(self, new_artist):
        self.artist = new_artist

    def get_art(self):
        return self.art

    def get_length(self):
        return self.length
