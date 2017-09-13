"""
Defines the centerline class - which should have methods that can describe the given curve
 -Needs to take care of the references to points on line - that includes lenght, t, and points
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
