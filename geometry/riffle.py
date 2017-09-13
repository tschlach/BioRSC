"""
Defines the riffle class
"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

class Riffle(object):
    """  
	"""
	def __init__(self, centerline, start, drop, run, width, depth):
		self.curve = centerline #user input centerline of the stream
		self.start = start
		self.drop = drop
		self.run = run #is 'run' the same thing as 'length'? or is it the 'horizontal' distance...
		self.width = width
		self.depth = depth

	def draw_riffle(self):
		return riffle
		###This function should replicate the grasshopper components that 'draw' the riffles
		