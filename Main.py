import sys
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import QUrl, QDirIterator, Qt, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QWidget, QInputDialog, QLineEdit, QLabel
import SongDatabase
from mutagen import File

# TODO: Add search functionality to show results to user
# TODO: Add  more songs to test functionality
# TODO: Allow user to remove songs


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()        # QMediaPlayer class allows the playing of a media source.
        self.playlist = QMediaPlaylist()    # QMediaPlaylist class provides a list of media content to play.
        self.title = 'SpotiPy'
        self.left = 300
        self.top = 300
        self.width = 300
        self.height = 150
        self.color = 0  # 0- toggle to dark 1- toggle to light
        self.userAction = -1  # 0- stopped, 1- playing 2-paused
        self.setup_UI()
        self.my_songs = []
        self.user_row_clicked = []
        self.highlighted_row = None
        self.metadata = File("python.jpg")

    def setup_UI(self):
        # Add file menu
        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        windowmenu = menubar.addMenu('Window')

        help_act = QAction('Open Help', self)
        folder_act = QAction('Open Folder', self)
        theme_act = QAction('Toggle light/dark theme', self)

        folder_act.setShortcut('Ctrl+D')
        help_act.setShortcut('Ctrl+H')
        theme_act.setShortcut('Ctrl+T')

        filemenu.addAction(folder_act)
        filemenu.addAction(help_act)
        windowmenu.addAction(theme_act)

        help_act.triggered.connect(self.open_help)
        folder_act.triggered.connect(self.add_files)
        theme_act.triggered.connect(self.toggle_colors)

        self.createTable()
        # self.getText()
        self.add_controls()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.toggle_colors()
        self.show()

    def add_controls(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.label = QLabel()

        # Add song controls
        volumeslider = QSlider(Qt.Horizontal, self)
        volumeslider.setFocusPolicy(Qt.NoFocus)
        volumeslider.valueChanged[int].connect(self.change_volume)
        volumeslider.setValue(100)

        play_btn = QPushButton('Play')  # play button
        pause_btn = QPushButton('Pause')  # pause button
        stop_btn = QPushButton('Stop')  # stop button

        # Add playlist controls
        prev_btn = QPushButton('Prev')
        shuffle_btn = QPushButton('Shuffle')
        next_btn = QPushButton('Next')
        sort_btn = QPushButton('Sort')
        search_btn = QPushButton('Search')
        remove_btn = QPushButton('Remove')

        # Add button layouts
        control_area = QVBoxLayout()  # centralWidget
        controls = QHBoxLayout()
        playlist_ctrl_layout = QHBoxLayout()
        playlist_func = QHBoxLayout()

        self.show_cover_art()

        self.cb1 = QComboBox()
        self.cb1.addItem("Sort by Title")
        self.cb1.addItem("Sort by Album")
        self.cb1.addItem("Sort by Artist")
        self.cb1.currentIndexChanged.connect(self.selectionchange)

        self.cb2 = QComboBox()
        self.cb2.addItem("Search by Title")
        self.cb2.addItem("Search by Album")
        self.cb2.addItem("Search by Artist")
        self.cb2.currentIndexChanged.connect(self.selectionchange)

        # Add buttons to song controls layout
        controls.addWidget(play_btn)
        controls.addWidget(pause_btn)
        controls.addWidget(stop_btn)

        # Add buttons to playlist controls layout
        playlist_ctrl_layout.addWidget(prev_btn)
        playlist_ctrl_layout.addWidget(shuffle_btn)
        playlist_ctrl_layout.addWidget(next_btn)

        # playlist_func.addWidget(sort_btn)
        playlist_func.addWidget(search_btn)
        playlist_func.addWidget(remove_btn)
        # playlist_func.addWidget(QInputDialog)

        # bottom_func.addWidget(self.cb1)
        # bottom_func.addWidget(self.label)

        # Add to vertical layout
        control_area.addLayout(controls)
        control_area.addLayout(playlist_ctrl_layout)
        control_area.addLayout(playlist_func)
        control_area.addWidget(volumeslider)
        control_area.addWidget(self.tableWidget)
        # control_area.addWidget(self.combos)
        control_area.addWidget(self.cb1)
        control_area.addWidget(self.label)
        # control_area.addWidget(bottom_func)
        wid.setLayout(control_area)

        # Connect each signal to their appropriate function
        play_btn.clicked.connect(self.play_handler)
        pause_btn.clicked.connect(self.pause_handler)
        stop_btn.clicked.connect(self.stop_handler)

        prev_btn.clicked.connect(self.prev_song)
        shuffle_btn.clicked.connect(self.shuffle_list)
        next_btn.clicked.connect(self.next_song)

        sort_btn.clicked.connect(self.sort_handler)
        search_btn.clicked.connect(self.search_handler)
        remove_btn.clicked.connect(self.remove_handler)

        self.statusBar()
        # Signal emitted when current media changes. Call song_changed
        self.playlist.currentMediaChanged.connect(self.song_changed)

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)

        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Title")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        item.setText("Artist")
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        item.setText("Album")
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        item.setText("Length")
        self.tableWidget.setHorizontalHeaderItem(3, item)

        # Don't allow user to edit
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        # Make columns fit window size
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.tableWidget.move(0, 0)

        # table selection change
        current_row = self.tableWidget.itemClicked.connect(self.on_click)
        print("ret var ", current_row)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        # self.highlighted_row = None  # Avoids reference before assignment
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.highlighted_row = currentQTableWidgetItem.row()
            print(self.highlighted_row, currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            # Call func in SongDatabase to compare
            self.tableWidget.selectRow(self.highlighted_row)
            SongDatabase.SongDatabase.find_song_to_play(my_songs=self.my_songs, search_song=currentQTableWidgetItem.text())
            self.user_row_clicked.append(self.highlighted_row)
        return self.highlighted_row

    def sort_handler(self):
        pass

    def search_handler(self):
        text, ok_pressed = QInputDialog.getText(self, "Search", "Filter:", QLineEdit.Normal, "")
        if ok_pressed and text != '':
            print("Searching for: ", text)
            SongDatabase.SongDatabase.filter_songs_search(self.my_songs, text)

    def remove_handler(self):
        self.player.playlist().removeMedia(self.highlighted_row)    # remove from playlist
        print("removed row: ", self.highlighted_row, "Song: ", self.my_songs[self.highlighted_row].get_title())
        del self.my_songs[self.highlighted_row]     # remove from list
        self.populate_table(self.my_songs)
        pass

    def selectionchange(self, i):
        print("Items in the list are :")

        for count in range(self.cb1.count()):
            print(self.cb1.itemText(count))
        print("Current index", i, "selection changed ", self.cb1.currentText())

    @staticmethod
    def open_help():
        choice = QMessageBox.question(None, 'Help', 'This application was developed by Ryan Rizzo as part of the'
                                                    ' Software for Engineers Course', QMessageBox.Ok)

        if choice == QMessageBox.Ok:
            pass

    def add_files(self):
        # If playlist contains songs, simply call folder_iterator
        if self.playlist.mediaCount() != 0:
            self.folder_iterator()
        # If playlist does not contain songs, call folder_iterator and create new playlist
        else:
            self.folder_iterator()
            self.player.setPlaylist(self.playlist)
            # The player object will use the current playlist item for selection of the content to be played.
            # detCurrentIndex() activates media content from playlist at position playlistPosition.
            self.player.playlist().setCurrentIndex(0)
            # Start or resume playing the current source.
            self.player.play()
            self.userAction = 1

    def folder_iterator(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        folder_directory = QFileDialog.getExistingDirectory(None, "Find Files", "All Files (*);;Python Files (*.py)",
                                                            options=options)

        print(folder_directory)

        self.my_songs = SongDatabase.SongDatabase.retrieve_songs(directory=folder_directory)
        print(self.my_songs)
        total = SongDatabase.SongDatabase.print_song_info(my_songs=self.my_songs)
        self.populate_table(self.my_songs)

        for i in range(len(self.my_songs)):
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.my_songs[i].get_path())))

    def populate_table(self, my_songs):
        # clear all rows to re-populate
        self.tableWidget.setRowCount(0)
        for row, data in enumerate(my_songs):
            # print("ROW: ", row)

            self.tableWidget.insertRow(self.tableWidget.rowCount())

            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(my_songs[row].get_title())
                                                              .strip('"\'')))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(my_songs[row].get_artist())
                                                              .strip('"\'')))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(my_songs[row].get_album())
                                                              .strip('"\'')))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(my_songs[row].get_length())
                                                              .strip('"\'')))

    def show_cover_art(self):
        pixmap = QPixmap()
        try:
            for tag in self.metadata.tags.values():
                if tag.FrameID == 'APIC':
                    pixmap.loadFromData(tag.data)
                    print("HERE (designer)")
                    break
        except AttributeError:
            print("No tags")

        pix_scaled = pixmap.scaled(256, 256, Qt.KeepAspectRatio)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(pix_scaled)

    def play_handler(self):
        """Handles playing of songs.
        1. If no playlist present, prompt user to load mp3 files
        2. If playlist present and user presses play, first song will play
        3. If playlist present and user clicks on song, and then presses play, desired song will play
        4. If song is paused and user presses play, paused song will resume."""

        # 4. Resuming paused song
        if self.userAction == 2:
            self.player.play()
            self.userAction = 1
        else:
            if self.playlist.mediaCount() == 0:
                # 1. if no songs in playlist prompt user to add files
                self.add_files()
            elif self.playlist.mediaCount() != 0:
                # 2. Playing first song if user has not clicked on table row
                if not self.user_row_clicked:
                    self.metadata = File(self.my_songs[0].get_path())
                    self.show_cover_art()
                    self.player.playlist().setCurrentIndex(0)
                    self.player.play()
                # 3. Playing desired song
                else:
                    # self.user_row_clicked[-1] contains last element in list
                    # index my_songs list with row user clicked to play desired song
                    play_song = self.user_row_clicked[-1]
                    print("Playing Row: ", play_song, self.my_songs[play_song].get_title())
                    # Set current playlist index to play song
                    self.player.playlist().setCurrentIndex(play_song)
                    self.metadata = File(self.my_songs[play_song].get_path())
                    self.show_cover_art()
                    self.player.play()
                    self.userAction = 1

    def pause_handler(self):
        self.userAction = 2
        self.player.pause()

    def stop_handler(self):
        self.userAction = 0
        self.player.stop()
        self.playlist.clear()
        self.statusBar().showMessage("Stopped and cleared playlist")

    def change_volume(self, value):
        self.player.setVolume(value)

    def prev_song(self):
        if self.playlist.mediaCount() == 0:
            self.add_files()
        elif self.playlist.mediaCount() != 0:
            self.player.playlist().previous()
            index = self.player.playlist().currentIndex()       # get current song index
            print(index)
            self.metadata = File(self.my_songs[index].get_path())     # update metadata
            self.show_cover_art()                               # display current song art

    def shuffle_list(self):
        self.playlist.shuffle()
        index = self.player.playlist().currentIndex()
        print(index)
        self.metadata = File(self.my_songs[index].get_path())
        self.show_cover_art()

    def next_song(self):
        if self.playlist.mediaCount() == 0:
            self.add_files()
        elif self.playlist.mediaCount() != 0:
            self.player.playlist().next()
            index = self.player.playlist().currentIndex()
            print(self.my_songs[index].get_path())
            self.metadata = File(self.my_songs[index].get_path())
            self.show_cover_art()

    def song_changed(self, media):
        # if media is available, display URL on status bar
        if not media.isNull():
            url = media.canonicalUrl()
            self.statusBar().showMessage(url.fileName())

    def toggle_colors(self):
        """ Fusion dark palette from https://gist.github.com/QuantumCD/6245215. Modified by me and J.J. """
        app.setStyle("Fusion")
        palette = QPalette()
        if self.color == 0:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(235, 101, 54))
            palette.setColor(QPalette.Highlight, QColor(235, 101, 54))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.color = 1
        elif self.color == 1:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, Qt.white)
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(66, 155, 248))
            palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            self.color = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
sys.exit(app.exec_())