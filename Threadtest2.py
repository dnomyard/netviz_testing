#!/usr/bin/python

"""
http://code.activestate.com/recipes/82965-threads-tkinter-and-asynchronous-io/

This recipe describes how to handle asynchronous I/O in an environment
where you are running PyQt as the graphical user interface. PyQt is
safe to use as long as all the graphics commands are handled in a
single thread. Since it is more efficient to make I/O channels to
block and wait for something to happen rather than poll at regular
intervals, we want I/O to be handled in separate threads. These can
communicate in a threasafe way with the main, GUI-oriented process
through one or several queues. In this solution the GUI still has to
make a poll at a reasonable interval, to check if there is something
in the queue that needs processing. Other solutions are possible, but
they add a lot of complexity to the application.

Created by Jacob Halln, AB Strakt, Sweden. 2001-10-17
Adapted by Boudewijn Rempt, Netherlands. 2002-04-15
Updated to Qt 4.7 by Dirk Swart, Ithaca, NY. 2011-04-15
"""

import sys, time, threading, random, Queue
from PyQt4 import QtGui, QtCore as qt



# drr
from scapy.all import *


class GuiPart(QtGui.QWidget):

    def __init__(self, queue, endcommand, *args):

        super(GuiPart, self).__init__()

        self.queue = queue
        # We show the result of the thread in the gui, instead of the console

        filterLabel=QtGui.QLabel('Filter')
        filterEdit=QtGui.QLineEdit()

        quitButton = QtGui.QPushButton('Quit', self)
        quitButton.clicked.connect(qt.QCoreApplication.instance().quit)

        self.editor = QtGui.QTextEdit(self)

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(filterLabel, 1, 0)
        self.grid.addWidget(filterEdit, 1, 1)

        self.grid.addWidget(self.editor, 2, 0, 5, 2)
        self.grid.addWidget(quitButton, 7, 0, 1, 2)

        self.setLayout(self.grid)
        self.setGeometry(300, 300, 500, 300)

        print 'here'

        # self.setCentralWidget(self.editor)
        self.endcommand = endcommand



    def closeEvent(self, ev):
        """
        We just call the endcommand when the window is closed
        instead of presenting a button for that purpose.
        """
        self.endcommand()

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                self.editor.insertPlainText(str(msg))
            except Queue.Empty:
                pass


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self):
        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui=GuiPart(self.queue, self.endApplication)
        self.gui.show()

        # A timer to periodically call periodicCall :-)
        self.timer = qt.QTimer()
        qt.QObject.connect(self.timer,
                           qt.SIGNAL("timeout()"),
                           self.periodicCall)
        # Start the timer -- this replaces the initial call to periodicCall
        self.timer.start(100)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()


    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            root.quit()

    def endApplication(self):
        self.running = 0

    def testTTL(self, pkt):
        try:
            if pkt.haslayer(IP):
                ipsrc=pkt.getlayer(IP).src
                ttl = str(pkt.ttl)
                msg = '[+] Pkt Received From: '+ipsrc+' with TTL: '+ ttl + '\n'
                self.queue.put(msg)

        except:
            pass


    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        sniff(prn=self.testTTL, store=0)

        # while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.

            # time.sleep(rand.random() * 0.3)
            # msg = rand.random()
            # self.queue.put(msg)




def main():

    root = QtGui.QApplication(sys.argv)
    client = ThreadedClient()
    sys.exit(root.exec_())




if __name__ == '__main__':

    main()



