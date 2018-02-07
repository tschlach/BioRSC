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
T_RS = []
T_RE = []
T_PS = []
T_PE = []
widths = []

for i in crvRifflePoints.riffles:
   if i.use == 1:
	   pRS.append(i.ptBankMin)
	   pRE.append(i.riffle.pt_end)
	   pPS.append(i.pool.pt_start)
	   pPE.append(i.pool.pt_end)
	   paramaters.append(i.parameter)
	   lengths.append(i.riffle.length)
	   drops.append(i.riffle.drop)
	   T_RS.append(i.tangent)
	   T_RE.append(i.riffle.tangent_end)
   	   T_PS.append(i.pool.tangent_start)
   	   T_PE.append(i.pool.tangent_end)	
	   widths.append(i.riffle.width)

for i in crvRifflePoints.riffles:
    pAll.append(i.ptBankMin)

t = paramaters
riffle_length = lengths
riffle_drop = drops
riffle_width = widths
T_rStart = T_RS
T_rEnd = T_RE
T_pStart = T_PS
T_pEnd = T_PE
pts_rStart = pRS
pts_rEnd = pRE
pts_pStart = pPS
pts_pEnd = pPE
allpts = pAll
