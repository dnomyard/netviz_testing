#!/usr/bin/python

import sys
import urllib2

from PyQt4 import QtCore, QtGui


class DownloadThread(QtCore.QThread):
    def __init__(self, url, list_widget):
        QtCore.QThread.__init__(self)
        self.url = url
        self.list_widget = list_widget

    def run(self):
        info = urllib2.urlopen(self.url).info()
        self.list_widget.addItem('%s\n%s' % (self.url, info))


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.list_widget = QtGui.QListWidget()
        self.button = QtGui.QPushButton("Start")
        self.button.clicked.connect(self.start_download)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def start_download(self):
        urls = ['http://google.com', 'http://twitter.com', 'http://yandex.ru',
                'http://stackoverflow.com/', 'http://www.youtube.com/']
        self.threads = []
        for url in urls:
            downloader = DownloadThread(url, self.list_widget)
            self.threads.append(downloader)
            downloader.start()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
