"""
Defines the centerline class - which should have methods that can describe the given curve
 -Needs to take care of the references to points on line - that includes lenght, t, and points
"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

class Centerline(object):
	def __init__(self, length, parameters, pts):
