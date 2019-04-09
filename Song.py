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

    def get_album(self):
        return self.album

    def get_artist(self):
        return self.artist

    def get_art(self):
        return self.art

    def get_length(self):
        return self.length


# song = Song()