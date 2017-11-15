import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 


points = []
paramaters = []
lengths = []
drops = []
tangents = []

for i in Riffles:
   points.append(i.pt)
   paramaters.append(i.parameter)
   lengths.append(i.riffle_length)
   drops.append(i.riffle_drop)
   tangents.append(i.tangent)

print(Riffles)


pts = points
t = paramaters
riffle_length = lengths
riffle_drop = drops
T = tangents
