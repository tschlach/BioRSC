"""
This file defines the 'window' class - which will be used to make assessments of suitability for riffles along a centerline curve
The script should be pasted into a Python component in Grasshopper, and takes the following inputs:
    crv: any curve
    window_start: the point on the line to begin the suitability assessment window
    window_width: the number of points in the window, each point = 0.5ft in length
"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

##Creates the Window class
class Window(object):
    def __init__(self, curve, start, curve_pts, span):
        self.curve = curve
        self.start_index = start
        self.curve_pts = curve_pts
        self.span = span
        self.start_pt = curve_pts[start]
        self.window_pts = []
        self.end_pt = 0
        self.length = span/2 
    
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

##TBD curviness indicator
#    def curviness(self): 

###TBD apply weights to window attributes to output suitability metric
#    def suitability(self,numb_riffles): #the method that combines measurements in the window into a single suitability measure
#        curves = self.curviness()
#        slope = self.slope()
#        drop = self.drop()
#        return 
