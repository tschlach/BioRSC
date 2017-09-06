import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


###Input variables needed to draw a series of riffles: 
###start_points: list of user defined riffle start points
start_points = []


###should think about whether this needs to be a class - or just a function within the Riffle class
###need to divide line and get the output values of the divided line that gh outputs...
class SuitabilityWindow(object):
	"""  
	"""
	def __init__(self, size):
		self.size = size

	def slope():
		return avg_slope

	def bend():
		return 'bendy-ness' ###how to measure bendy-ness?

	def depth()


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

	def assess_riffle():
		###This function will assess the qualities of a riffle that is to be drawn at a given location
		###self.run (or self.length) is used to examine the points along the line - here we can call an instance
		###of a suitability window
		window = SuitabilityWindow()


	def draw_riffle():
		###This function will use rhinoscript syntax and other methods to replicate


for i in start_points:
	riff = Riffle(i,,,,)
	riff.draw_riffle()
