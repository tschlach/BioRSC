import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 


points = []
paramaters = []
lengths = []
drops = []
tangents = []

for i in crvRifflePoints.riffles:
   if i.use == 1:
	   points.append(i.ptBankMin)
	   paramaters.append(i.parameter)
	   lengths.append(i.riffle.length)
	   drops.append(i.riffle.drop)
	   tangents.append(i.tangent)


pts = points
t = paramaters
riffle_length = lengths
riffle_drop = drops
T = tangents
