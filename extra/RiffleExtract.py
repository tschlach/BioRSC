import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 


pRS = []
pRE = []
pPS = []
pPE = []
pAll = []
paramaters = []
lengths = []
drops = []
tangents = []

for i in crvRifflePoints.riffles:
   if i.use == 1:
	   pRS.append(i.ptBankMin)
	   pRE.append(i.riffle.pt_end)
	   pPS.append(i.pool.pt_start)
	   pPE.append(i.pool.pt_end)
	   paramaters.append(i.parameter)
	   lengths.append(i.riffle.length)
	   drops.append(i.riffle.drop)
	   tangents.append(i.tangent)

for i in crvRifflePoints.riffles:
    pAll.append(i.ptBankMin)

t = paramaters
riffle_length = lengths
riffle_drop = drops
T = tangents
pts_rStart = pRS
pts_rEnd = pRE
pts_pStart = pPS
pts_pEnd = pPE
allpts = pAll
