#!/usr/bin/python
import Tkinter as tk
import numpy
from random import randint
import sys, os
from scapy.all import *


class Netviz_test(tk.Frame):
    """
    MarruSim class extends tk.Frame for GUI
    """
        
    class Switch():
        """
        Switch class defines location of switches in Netviz environment
        """
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Computer():
        """
        Computer class defines location of workstations in Netviz environment
        """
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Tap():
        """
        Tap changes color if filter criteria is met
        """
        def __init__(self, x, y):
            self.x = x
            self.y = y

        
    def __init__(self, max_x, max_y, master=None):
        """
        Initilize NetViz GUI using tk
        """
        tk.Frame.__init__(self, master)
        self.max_x = max_x
        self.max_y = max_y
        self.grid()
        self.createWidgets()

        self.flag = True

        self.s1 = self.Switch(200, self.max_y/4)
        self.c1 = self.Computer(200, (3*(self.max_y/4)))
        self.t1 = self.Tap(200, self.max_y/2)

        edge = 10

        s1 = self.s1
        c1 = self.c1
        t1 = self.t1

        s1_img = self.canvas.create_bitmap(s1.x, s1.y, bitmap="@./switch.xbm", tag='s1')

        c1_img = self.canvas.create_bitmap(c1.x, c1.y, bitmap="@./computer.xbm", tag='c1')

        t1 = self.canvas.create_rectangle((t1.x-edge), (t1.y-edge), (t1.x + edge), (t1.y + edge), fill="red", tag='tap1')

        self.master.title('NetViz')
        # self.addStations()
		
    def createWidgets(self):
        """ Create canvas and buttons on tk frame. """
        self.canvas = tk.Canvas(self, width = self.max_x, height = self.max_y, background='white')
        self.canvas.pack()
        self.canvas.grid()
        # quit button not working - TODO
        # self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        # self.quitButton.grid()
        self.filterEntry = tk.Entry(self)
        self.filterEntry.grid()
        self.filterEntry.insert(0, "Enter filter")

        def callback():
            print self.filterEntry.get()

        self.filterButton = tk.Button(self, text="Filter", width=10, command=callback)
        self.filterButton.grid()

        self.textWindow = tk.Text(self)
        self.textWindow.grid()


    def quit(self):
        """ Flag boolean is used to stop simulation. """
        self.flag = False
        tk.Frame.quit(self)


    def testTTL(pkt):
        try:
            if pkt.haslayer(IP):
                ipsrc=pkt.getlayer(IP).src
                ttl = str(pkt.ttl)
                self.textWindow.insert(END, ttl)

        except:
            pass


    def getPackets(self):
        """ display packets to textWindow """

        numPkts = 0

        sniff(prn=testTTL, store=0)

            

        
    def addStations(self):
        """ Create end stations and place on canvas. """
        # size of stations in pixels
        edge = 20
        # station 1: left side of of canvas
        s1 = self.Station(100, self.max_y/2)
        station1 = self.canvas.create_rectangle(s1.x, s1.y, (s1.x + edge), (s1.y + edge), fill="red", tag='station1')
        self.text1 = self.canvas.create_text(s1.x + 5, s1.y + 32, tag = "rssi1_label")
        
        # station 2: right side of canvas
        s2 = self.Station(self.max_x - 100, self.max_y/2)
        station2 = self.canvas.create_rectangle(s2.x, s2.y, (s2.x + edge), (s2.y + edge), fill="green", tag='station2')
        self.text2 = self.canvas.create_text(s2.x + 5, s2.y +32, tag = "rssi2_label")
        
        self.s1 = s1
        self.s2 = s2



if __name__ == "__main__":
    """ 
    The MarruSim class should be imported and used from an external Python
    program.  If MaruuSim is executed independently, we simply run randomTest.
    """
    app = Netviz_test(600, 600)
    app.mainloop()

    app.getPackets()
