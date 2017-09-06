"""
This file defines the 'window' class - which will be used to make assessments of suitability for riffles along a centercurve line
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

class Window(object):
    def __init__(self, start, curve, pts, span):
        self.start = start
        self.curve = curve
        self.pts = pts
        self.span = span
    
    def generate(self):
        points = []
        for i in range(self.span):
            points.append(self.pts[self.start+i])
        return points

    def slope(self):
    	return slope # returns the slope of the window from  the start point to the end point (start+span)

window = Window(window_start, crv, pts, window_width)

window_out = window.generate()

###Next, we need to:
#
##	-write a method for 'evaluating' slope
##  -write other methods...
##  -make more detailed comments throughout - documentation...
##
##
##
#
