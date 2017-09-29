"""
Author: Biohabitats Inc.
Updated: September 29, 2017

Defines the riffle class

Tasks:
	-draw_riffle method:
		1. window start and ends
		2. depth in the z-vector
		3. draw 2 points of distance width/2 from the centerline, perpendicular to the centerline
		4. draw an arc between the 3 points

"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

class Riffle(window):
    """  
	"""
	def __init__(self, centerline, width, depth):
		self.curve = centerline #user input centerline of the stream
		self.start = start
		self.drop = drop
		self.run = run #is 'run' the same thing as 'length'? or is it the 'horizontal' distance...
		self.width = width
		self.depth = depth

	def draw_riffle(self):
		left_pt =
		right_pt =
		center_pt =
		window_curve = 
		arc = rs.AddArc3pt(left_pt, right_pt, center_pt) #take start point, riffle depth and riffle width
		riffle = rs.AddSweep1(window_curve, arc)
		return riffle
		###This function should replicate the grasshopper components that 'draw' the riffles
		