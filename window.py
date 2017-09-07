"""
This file defines the 'window' class - which will be used to make assessments of suitability for riffles along a centerline curve
The script should be pasted into a Python component in Grasshopper, and takes the following inputs:
    crv: any curve
    window_start: the point on the line to begin the suitability assessment window
    window_width: the number of points in the window, each point = 0.5ft in length
"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

############
#
#pre class definition variables - to be made into centerline class and passed into a window object
#
############
#number of segments line divided into - based on 1 segment every .5ft
segs = int(rs.CurveLength(crv) * 2)
#creates a list of points along the input curve - which will be used to create the window
pts = rs.DivideCurve(crv, segs)
# defines the parameters along the curve that match each of the pt locations
params = []
for i in pts:
    params.append(rs.CurveClosestPoint(crv,i))
#    
planes = []
for i in pts:
    planes.append(rs.PlaneFromPoints(i, ((1.0, 0.0, 0.0)),((0.0, 1.0, 0.0))))
############
#
#
############


##Creates the Window class
class Window(object):
    def __init__(self, start, curve, pts, span):
        self.start = start
        self.curve = curve
        self.pts = pts
        self.span = span
    
#generates a list of points that is the window
    def generate(self):
        window = []
        for i in range(self.span):
            window.append(self.pts[self.start+i])
        return window

# returns the overall slope of the window (drop/run)
    def slope(self):
        window = self.generate()
        s = 0
        for i in range(len(window)-1):
            drop = rs.Angle(window[i], window[i+1], rs.WorldXYPlane)[4]
            s += drop
        return s/(self.span/2)

# returns the total drop along the curve within the window
    def drop(self):
        window = self.generate()
        z = []
        for i in window:
            z.append(i[2])
        drop = z[0] - z[-1]
        return drop

##TBD curviness indicator
    def curviness(self): 

###TBD apply weights to window attributes to output suitability metric
    def suitability(self): #the method that combines measurements in the window into a single suitability measure
        curves = self.curviness()
        slope = self.slope()
        drop = self.drop()

        ###the rest of the function assesses the suitability of the window for riffle/pool

window = Window(window_start, crv, pts, window_width)

###set your output - can be generate, pts, drop etc...

window_out = window.generate()
