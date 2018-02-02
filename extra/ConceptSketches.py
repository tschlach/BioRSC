import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 

riffleLeft = []
riffleRight = []
riffleEnd = []

poolStart = []
poolEnd = []
poolMid = []
ptsPoolEnd = []
ptsStationMid = []
poolMidLeft = []
poolMidRight = []

text = []

for i in ctrlnStream.riffles:
	if i.use == 1:

		#RIFFLES
		#Check to see if there is a riffle Width - Default to 0 if none
		if i.riffle.width == None: i.riffle.width = 10
		
		#Riffle Right Point at start of Riffle
		pointRight = rs.AddPoint(i.riffle.pt_start.X + i.riffle.width / 2 * -i.tangent[1], i.riffle.pt_start.Y + i.riffle.width / 2 * i.tangent[0], i.riffle.pt_start.Z)
		riffleRight.append(pointRight)
		
		#Riffle Left Point at start of Riffle
		pointLeft = rs.AddPoint(i.riffle.pt_start.X + i.riffle.width / 2 * i.tangent[1], i.riffle.pt_start.Y + i.riffle.width / 2 * -i.tangent[0], i.riffle.pt_start.Z)
		riffleLeft.append(pointLeft)
		
		#Riffle End point at end of riffle
		riffleEnd.append(i.riffle.pt_end)
		print(i.riffle.width)
	   

		#POOLS
		#pool start
		poolStart.append(i.pool.pt_start)

		#pool End
		poolEnd.append(i.pool.pt_end)
		print('poolend=', i.pool.station_end)

		#pool Mid Left
		stationMid = (i.pool.station_start + i.pool.station_end) / 2
		print('poolmid=', stationMid)
		ptsStationMid = rs.DivideCurveLength(crvThalweg, stationMid, True, True)
		ptStationMid = ptsStationMid[1]
		parameter = rs.CurveClosestPoint(crvThalweg, ptStationMid)     #Parameter (t) for point on centerline
		tangent = rs.CurveTangent(crvThalweg, parameter)
		ptPoolMid = rs.AddPoint(ptStationMid.X + i.riffle.width / 2 * -tangent[1], ptStationMid.Y + i.riffle.width / 2 * tangent[0], i.pool.pt_start.Z)
		poolMidLeft.append(ptPoolMid)

		#pool Mid Right
		ptPoolMid = rs.AddPoint(ptStationMid.X + i.riffle.width / 2 * tangent[1], ptStationMid.Y + i.riffle.width / 2 * -tangent[0], i.pool.pt_start.Z)
		poolMidRight.append(ptPoolMid)

		string = 'STA:', i.station, 'invert:', round(i.ptBankMin.Z, 1), '; Riffle Length:', i.riffle.length, '; Riffle Drop:', i.riffle.drop, '; Pool Length:', round(i.pool.length, 1)
		text.append(string)
