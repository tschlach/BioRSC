"""
Author: Biohabitats Inc.
Updated: September 28, 2017

Defines the centerline class, the attributes of which can be used to inform the window class when making a suitability assessment

Inputs
	curve: a single Rhino curve

Tasks:
	-should the window class inherent Centerline attributes

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
        self.p_range = 0
        self.slopes = []
		self.curve = curve
		
	def getParameters(self):
	    for i in self.points:
	        self.parameters.append(rs.CurveClosestPoint(self.curve, i))
	    self.p_range = abs(self.parameters[0] - self.parameters[-1])
	    return

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
