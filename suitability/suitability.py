"""
This script takes class definitions (window and centerline) and adds the functional components that make the thing actually run in a grasshopper script...
	Needs:
		-A subfolder in the BioRSC repository, with a screenshot of a grasshopper layout that makes the script functional... 
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

class Centerline(object):
	def __init__(self, curve):
		self.length = rs.CurveLength(curve)
		self.start = rs.CurveStartPoint(curve)
		self.end = rs.CurveEndPoint(curve)
		self.drop = self.start[2] - self.end[2]
		self.segments = self.length * 2
		self.points = rs.DivideCurve(curve, self.segments)
		self.parameters = []
		self.curve = curve
		
	def getParameters(self):
	    for i in self.points:
	        self.parameters.append(rs.CurveClosestPoint(self.curve, i))
	    return

class Window(object):
    def __init__(self, curve, start, curve_pts, span):
        self.curve = curve
        self.start_index = start
        self.curve_pts = curve_pts
        self.span = span
        self.start_pt = curve_pts[start]
        self.window_pts = []
        self.end_pt = 0
        self.length = span/2 ###span is the number of points in the window...we divide by 2 because each point is 1/2 ft appart...
    
    def generate(self):
        window = []
        for i in range(self.span):
            window.append(self.curve_pts[self.start_index+i])
        self.window_pts = window
        self.end_pt = window[-1]
        self.drop = self.start_pt[2] - self.end_pt[2]
        self.slope = self.drop/self.length
        return

curve = Centerline(crv)

window = Window(curve.curve, window_start, curve.points, window_width)

window.generate()