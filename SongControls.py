# from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
# from PyQt5.QtGui import QPalette, QColor
# from PyQt5.QtCore import QUrl, QDirIterator, Qt
# from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, \
#     QVBoxLayout, QSlider, QMessageBox
#
#
# class Controls:
#     def __init__(self):
#         self.player = QMediaPlayer()  # QMediaPlayer class allows the playing of a media source.
#         self.playlist = QMediaPlaylist()  # QMediaPlaylist class provides a list of media content to play.
#         self.userAction = -1  # 0- stopped, 1- playing 2-paused
#
#     def play_handler(self):
#         if self.playlist.mediaCount() == 0:
#             # if no songs in playlist prompt user to add files
#             self.add_files()
#         elif self.playlist.mediaCount() != 0:
#             # if songs in playlist play current song
#             self.player.play()
#             self.userAction = 1
#
#     def add_files(self):
#         # If playlist contains songs, simply call folder_iterator
#         if self.playlist.mediaCount() != 0:
#             self.folder_iterator()
#         # If playlist does not contain songs, call folder_iterator and create new playlist
#         else:
#             self.folder_iterator()
#             self.player.setPlaylist(self.playlist)
#             # The player object will use the current playlist item for selection of the content to be played.
#             # detCurrentIndex() activates media content from playlist at position playlistPosition.
#             self.player.playlist().setCurrentIndex(0)
#             # Start or resume playing the current source.
#             self.player.play()
#             self.userAction = 1
#
#     def folder_iterator(self):
#         options = QFileDialog.Options()
#
#         options |= QFileDialog.DontUseNativeDialog
#         folder_directory = QFileDialog.getExistingDirectory(None, "Find Files", "All Files (*);;Python Files (*.py)",
#                                                             options=options)
#         if folder_directory != None:
#             # QDirIterator class provides an iterator for directory entrylists.
#             it = QDirIterator(folder_directory)
#             it.next()   # next() function returns the path to the next directory entry and advances the iterator.
#             # hasNext() returns true if there is at least one more entry in the directory; otherwise, false is returned.
#             while it.hasNext():
#                 # QFileInfo class provides system-independent file information.
#                 # isDir() returns true if this object points to a directory or to a symbolic link to a directory;
#                 # filePath() returns the file name, including the path (which may be absolute or relative).
#                 if it.fileInfo().isDir() == False and it.filePath() != '.':     # Path delimiter
#                     f_info = it.fileInfo()  # Access file information of current file
#                     if f_info.suffix() in 'mp3':    # Check for .mp3 suffix
#                         self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath()))) # add to playlist
#                 it.next()
#             if it.fileInfo().isDir() == False and it.filePath() != '.':
#                 f_info = it.fileInfo()
#                 if f_info.suffix() in 'mp3':
#                     self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
#
#     def pause_handler(self):
#         self.userAction = 2
#         self.player.pause()
#
#     def stop_handler(self):
#         self.userAction = 0
#         self.player.stop()
#         self.playlist.clear()
#         self.statusBar().showMessage("Stopped and cleared playlist")
#
#     def change_volume(self, value):
#         self.player.setVolume(value)
#
#     def prev_song(self):
#         if self.playlist.mediaCount() == 0:
#             self.add_files()
#         elif self.playlist.mediaCount() != 0:
#             self.player.playlist().previous()
#
#     def shuffle_list(self):
#         self.playlist.shuffle()
#
#     def next_song(self):
#         if self.playlist.mediaCount() == 0:
#             self.add_files()
#         elif self.playlist.mediaCount() != 0:
#             self.player.playlist().next()
#
#     def song_changed(self, media):
#         # if media is available, display URL on status bar
#         if not media.isNull():
#             url = media.canonicalUrl()
#             self.statusBar().showMessage(url.fileName())
#
#
# controls = Controls()
