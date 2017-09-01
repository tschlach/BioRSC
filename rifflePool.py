#This 'module' will define classes for 'riffles' and 'pools'. Riffles and pools are shapes to be drawn in Rhino though commands given in grasshopper. The 
#module is written in python - and should be able to be used 

"""
Riffle and pool construction using a stream as the input.
"""


###The input is a stream... there is only one stream instance. 
###We can call this class whatever we want - it's a centerline, it's a stream, it's a curve, it's a thalweg - the name here is arbitrary.
class centerLine():
	def __init__(self, start, end, length, slope):
		self.start =
		self.end =
		self.length = rs.



###When defining the riffle class - what are the imports that we're most interested in?
class riffle(start,end):
	start = #starting point of riffle, [x,y,z] 
	end = #ending point of riffle, [x,y,z] 
	length = #length along the riffle line

	def __init__(self, start, end):
		self.start = 

	def slope(self, start, end): ##Should slope be a method (function) or merely and attribute (variable)?? What are the 'pros and cons' - what do we need slope to do?

	def make_riffle(self): ##This should be the function that actually makes the riffle...
		#the make_riffle command will use geometry defined in the instance of the 


class pool():
	def __init__():

	def make_pool(self):
		###in here we put the commands needed to 'make the pool'


##Once we define the classes for riffles and pools. We need to make instances of those classes for the points