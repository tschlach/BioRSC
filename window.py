"""
This file defines the 'window' class - which will be used to make assessments of suitability for riffles along a centercurve line
The script can be loaded into a Python component in Grasshopper, and takes the following inputs:
    crv: any curve
    window_start: the point on the line to begin the window
    window_width: the number of points in (ie length of) the window
"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

###Variables that could be used by the window object class
##
segs = rs.CurveLength(crv) * 2
pts = rs.DivideCurve(crv, segs)
params = []
for i in pts:
    params.append(rs.CurveClosestPoint(crv,i))
planes = []
for i in pts:
    planes.append(rs.PlaneFromPoints(i, ((1.0, 0.0, 0.0)),((0.0, 1.0, 0.0))))
##


##Creates the Window class
class Window(object):
    def __init__(self, start, curve, pts, span):
        self.start = start
        self.curve = curve
        self.pts = pts
        self.span = span
    
    def generate(self): #generates a list of points that is the window
        window = []
        for i in range(self.span):
            window.append(self.pts[self.start+i])
        return window

    def slope(self): #returns the slope of the window between first and last point
        window = self.generate()
        s = []
        for i in window:
            slope = rs.Angle(window[i], window[i+1], rs.WorldXYPlane)
            s.append()
        return slope

    def drop(self): #returns the difference in z between first and last point in the window
        window = self.generate()
        z = []
        for i in window:
            z.append(i[2])
        drop = z[0] - z[-1]
        return drop

    def curviness(self):

    def suitability(self): #the method that combines measurements in the window into a single suitability measure
        curves = self.curviness()
        slope = self.slope()
        drop = self.drop()

        ###the rest of the function assesses the suitability of 

window = Window(window_start, crv, pts, window_width)

###set your output - can be generate, pts, drop etc...

window_out = window.generate() 