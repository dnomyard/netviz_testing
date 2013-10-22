#!/usr/bin/python
import Tkinter as tk
import numpy
from random import randint
import sys, os

class MaaruSim(tk.Frame):
    """
    MarruSim class extends tk.Frame for GUI
    """
    
    class Station():
        """
        Station class is used to define end stations in maaru simulation.
        """
        def __init__(self, x, y):
            """ Constructor sets initial x,y location for end stations. """
            self.x = x
            self.y = y
        
        def getRssi(self, copter):
            """ 
            RSSI is simulated using inverse distance from station to copter.
            """
            # Calculate distance between copter and end station.
            point_a = numpy.array((self.x, self.y))
            point_b = numpy.array((copter.x, copter.y))
            distance = numpy.sqrt(numpy.sum((point_a - point_b)**2))
            # RSSI = inverse distance with scaling factor (1/4 * PI * R^2)
            #r = int(1/distance * 100000)
            rssi = int(500000000/(4 * numpy.pi * distance * distance))
            return rssi

        def setStationRssiThreshold(self, rssi_val):
            """ Sets RSSI threshold for end station. """
            self.rssi_thresh = rssi_val
        
    class Copter():
        """ Used to maintain x, y location of copter. """
        
        def __init__(self, x, y):
            """ Initialize x, y location of copter. """
            self.x = x
            self.y = y

        def getLocation(self):
            """ Returns current location of copter. """
            return self.x, self.y
            

    def __init__(self, max_x, max_y, master=None):
        """
        Initilize simulation GUI using tk
        """
        tk.Frame.__init__(self, master)
        self.max_x = max_x
        self.max_y = max_y
        self.grid()
        self.createWidgets()
        self.thresholdMet = False
        self.flag = True
        # random starting location
        start_x = randint(100, self.max_x - 100)
        start_y = randint(100, self.max_y - 100)

        #start_x = 100
        #start_y = 100
        
        # create quadcopter object
        maaru = self.Copter(start_x, start_y)

        testcopter = self.canvas.create_bitmap(maaru.x, maaru.y, bitmap="@./copter.xbm", tag='maaru')
        self.maaru = maaru
        
        self.master.title('Maaru Simulator')
        self.addStations()
		
    def createWidgets(self):
        """ Create canvas and buttons on tk frame. """
        self.canvas = tk.Canvas(self, width = self.max_x, height = self.max_y, background='white')
        self.canvas.pack()
        self.canvas.grid()
        # quit button not working - TODO
        # self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        # self.quitButton.grid()
        self.resetButton = tk.Button(self, text='Reset', command=self.restart)
        self.resetButton.grid()
        
    def quit(self):
        """ Flag boolean is used to stop simulation. """
        self.flag = False
        tk.Frame.quit(self)

    def restart(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
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

    def setRssiThresholds(self, threshold):
        """ Set RSSI thresholds for both end stations. """
        # for now, assuming same RSSI threshold for both stations
        self.s1.setStationRssiThreshold(threshold)
        self.s2.setStationRssiThreshold(threshold)

    def checkThresholdMet(self):
        """ 
        Return value of Boolean, which is set when RSSI threshold is met.
        """
        # thresholdMet is a Boolean - True if RSSI values are above threshold; False if not
        #   This value is set in False in __init__() and set to true in moveToWaypoint()
        return self.thresholdMet

    def randomTest(self):
        """ 
        Test procedure has the copter flying around the canvas and 
        bouncing off walls.  It will stop if RSSI thresholds are met.
        """
        # initialize change in x, y
        dx = 2
        dy = 3
        # Initialize boundaries of maaru (x, y is center of copter, so
        # offsets are used to bounce edge of copter off of borders of
        # canvas instead of bouncing at the middle.
        x0 = self.maaru.x - 40
        x1 = self.maaru.x + 40
        y0 = self.maaru.y - 40
        y1 = self.maaru.y + 40

        # self.flag is a Boolean; set to True in __init__(); 
        # set to False when RSSI thresholds are met.
        while self.flag:
            # update maaru location
            self.canvas.move('maaru', dx, dy)
            self.canvas.after(20)
            self.canvas.update()
            self.maaru.x += dx
            self.maaru.y += dy
            rssi1 = self.s1.getRssi(self.maaru)
            rssi2 = self.s2.getRssi(self.maaru)
            
            # update rssi text boxes
            self.canvas.itemconfigure(self.text1, text="RSSI: " + str(rssi1))
            self.canvas.itemconfigure(self.text2, text="RSSI: " + str(rssi2))
            
            # copter bounces off of walls           
            if x1 >= self.max_x:
                dx = -2
            if y1 >= self.max_y:
                dy = -3
            if y0 < 0:
                dy = 3
            if x0 < 0:
                dx = 2
            x0 += dx
            x1 += dx
            y0 += dy
            y1 += dy

            # When RSSI values are met for both end stations, change
            # value of "quit" flag to False to stop copter.
            if rssi1 > self.s1.rssi_thresh and rssi2 > self.s2.rssi_thresh:
                print "Threshold met"
                self.flag = False

    def getLocation(self):
        """ Returns current x, y location of copter. """
        return self.maaru.getLocation()

    def moveToWaypoint(self, x, y):
        """ Moves copter to x/y values provided. """
        if x <= 0 or x >= self.max_x:
            print "moveToWaypoint: invalid value for x: " + str(x)
            return

        if  y <= 0 or y >= self.max_y:
            print "moveToWaypoint: invalid value for y: " + str(y)
            return

        # Calculate initial change in x, y based on direction
        # to waypoint.
        x_offset = x - self.maaru.x
        y_offset = y - self.maaru.y

        print 'x offset ' + str(x_offset)
        print 'y offset ' + str(y_offset)

        print 'x ' + str(x)
        print 'y ' + str(y)


        if abs(x_offset) >= abs(y_offset):
        
            print("HERE")
            slope = float(y_offset)/float(x_offset)
            
            print "slope: " + str(slope)
        
            # initialize change in x, y
            if x > self.maaru.x:            
                dx = float(2)
            else:
                dx = float(-2)
            dy = float(dx * slope)

        else:
            slope = float(x_offset)/float(y_offset)
            
            print "slope: " + str(slope)
        
            # initialize change in x, y
            if y > self.maaru.y:            
                dy = float(2)
            else:
                dy = float(-2)
            dx = float(dy * slope)
        



        print "dx: " + str(dx) + "    dy: " + str(dy)

        self.flag = True

        while self.flag:
            # Update maaru location.  
            # Here we are going to move toward specified waypoint unitl waypoint
            # is reached OR RSSI threshold is met.
            self.canvas.move('maaru', dx, dy)
            self.canvas.after(20)
            self.canvas.update()
            self.maaru.x += dx
            self.maaru.y += dy
            rssi1 = self.s1.getRssi(self.maaru)
            rssi2 = self.s2.getRssi(self.maaru)
            
            # update rssi text boxes
            self.canvas.itemconfigure(self.text1, text="RSSI: " + str(rssi1))
            self.canvas.itemconfigure(self.text2, text="RSSI: " + str(rssi2))

            deltaX = self.maaru.x - x
            deltaY = self.maaru.y - y
            # print "deltaX, deltaY: " + str(deltaX) + ", " + str(deltaY)
            if (deltaX < 2 and deltaX > -2) and (deltaY < 2 and deltaY > -2):
                print "Arrived at waypoint: " + str(x) + ", " + str(y)
                self.flag = False             

            if rssi1 > self.s1.rssi_thresh and rssi2 > self.s2.rssi_thresh:
                self.thresholdMet = True

if __name__ == "__main__":
    """ 
    The MarruSim class should be imported and used from an external Python
    program.  If MaruuSim is executed independently, we simply run randomTest.
    """
    app = MaaruSim(800, 600)
    app.setRssiThresholds(300)
    app.randomTest()
    app.mainloop()
