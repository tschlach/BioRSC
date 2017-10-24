"""
Title: BioRSC.py
Author: Biohabitats Inc.
Updated: October 24, 2017

Dependencies:
 - rhinoscriptsyntax as rs

This script contains the BioRSC library - and should consist of all components in the BioRSC tool.

"""
class Centerline(object):
    def __init__(self, curve):
        self.length = rs.CurveLength(curve)
        self.start = rs.CurveStartPoint(curve)
        self.end = rs.CurveEndPoint(curve)
        self.drop = self.start[2] - self.end[2]
        self.segments = self.length * 2 ##defines the number of segments for the self.points definition - here each segment is .5ft
        self.points = rs.DivideCurve(curve, self.segments)
        self.parameters = []
        self.p_range = 0
        self.p_ratios = [None, ] ##first point on the line has no p_ratio
        self.slopes = []
        self.curve = curve
    
    def getParameters(self):
        for i in self.points:
            self.parameters.append(rs.CurveClosestPoint(self.curve, i))
        self.p_range = abs(self.parameters[0] - self.parameters[-1])
        return

    def getPRatios(self): ## the 'local' p-ratio is 
        for i in range(1, len(self.parameters)-1):
            r = abs(self.parameters[i+1] - self.parameters[i-1])
            self.p_ratios.append(r) ##current p-ratio is r/span_of_local; span_of_local = 1
        self.p_ratios.append(None) ##the first and last index have a p_patio of none - because p ratios are a difference between

    #getSlopes defines the *discrete* slopes of the line, based on the straight distance between points on the line
    def getSlopes(self):
        for i in range(len(self.points) - 1):
            dx = self.points[i+1][0]- self.points[i][0]
            dy = self.points[i+1][1]- self.points[i][1]
            dz = self.points[i+1][2]- self.points[i][2]
            rise = dz
            run = math.sqrt(dx**2 + dy**2 + dz**2)
            slope = rise/run
            self.slopes.append(slope)
        return

class Window(object):
    def __init__(self, curve, start, curve_pts, span):
        self.curve = curve
        self.start_pt = start
        self.start_index = rs.PointArrayClosestPoint(curve_pts, start) ##gives index location of the window start along the curve
        self.curve_pts = curve_pts
        self.span = span
        self.window_pts = []
        self.parameters = []
        self.end_pt = 0
        self.length = span/2
        self.p_range = 0
        self.p_ratio = 0 ##a relative way of assessing the 'curviness' of a window

#a function that tests whether or not a given window start location attempts to generate a window that 'goes beyond' the length of the centerline
    def span_test(self): 
        window = []
        for i in range(self.span):
            try:
                window.append(self.curve_pts[self.start_index+i])                
            except Exception:
                print("Window is out of range for length " + str(self.length) + " feet.")
                return window
        return window

#generates a list of points that is the window - this is beginning to look like a second __init__ function...
    def generate(self, window):
        self.span = len(window)
        self.length = self.span/2
        self.window_pts = window
        self.end_pt = window[-1]
        self.drop = self.start_pt[2] - self.end_pt[2]
        self.slope = self.drop/self.length
        return

#constructs the p_range and p_ratio attributes of the window
    def getParameters(self):
        for i in self.window_pts:
            self.parameters.append(rs.CurveClosestPoint(self.curve, i))
        self.p_range = abs(self.parameters[0] - self.parameters[-1])
        self.p_ratio = self.p_range/self.length
        return
