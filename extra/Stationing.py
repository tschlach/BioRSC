import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 


ptsStationing = []
parameters = []
tangents = []
text = []



ptsStationing = rs.DivideCurveLength(crvCenterline, 25, True, True)


for i in range(len(ptsStationing)):
	parameter = rs.CurveClosestPoint(crvCenterline, ptsStationing[i])     #Parameter (t) for point on centerline
	parameters.append(parameter)
	tangents.append(rs.CurveTangent(crvCenterline, parameter))
	text.append(i*25)


t = parameters
T = tangents