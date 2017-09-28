"""
Author: Biohabitats Inc.
Updated: September 28, 2017

This file defines the 'window' class - which will be used to make assessments of suitability for riffles along a centerline curve
The script should be pasted into a Python component in Grasshopper

Inputs
    curve: the curve attribute of a centerline class (ie. Centerline.curve, redundant)
    start: a grasshopper 3d Point location, ideally set by user input
    curve_pts: the points attribute of a centerline class (ie. Centerline.points)
    span: the number of points along the line to include in the window - under current (Sep2017) Centerline class definition, points are spaced .5ft apart. As such, a span of 40 = 20ft window

Tasks:

"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

##Creates the Window class with a wide array of descriptive attributes - for 
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
    
#generates a list of points that is the window
    def generate(self):
        window = []
        for i in range(self.span):
            window.append(self.curve_pts[self.start_index+i])
        self.window_pts = window
        self.end_pt = window[-1]
        self.drop = self.start_pt[2] - self.end_pt[2]
        self.slope = self.drop/self.length
        return

    def getParameters(self):
        for i in self.window_pts:
            self.parameters.append(rs.CurveClosestPoint(self.curve, i))
        self.p_range = abs(self.parameters[0] - self.parameters[-1])
        self.p_ratio = self.p_range/self.length
        return