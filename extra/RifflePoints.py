import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 
#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy

#x = Thalweg2D - 2D representation of Crv
#y = Division lengths for points2D along centerline
#z = Right Bank 
#u = Left Bank


class Centerline(object):
    def __init__(self, crvCenterline, meshEX, crvBankRight, crvBankLeft, lenDivision):
        #****makes a list of each variable. In order, but not attributed to each point. 
        #****may want to pull everything under point info
        self.Thalweg2D = crvCenterline
        self.BankRight2D = crvBankRight
        self.BankLeft2D = crvBankLeft
        self.lenDivision = lenDivision
        self.riffles = []      
        
        self.length = rs.CurveLength(self.Thalweg2D)             #Length
        self.start = rs.ProjectPointToMesh(rs.CurveStartPoint(self.Thalweg2D), meshEX, (0,0,1))[0]          #3D Start Point
        self.end = rs.ProjectPointToMesh(rs.CurveEndPoint(self.Thalweg2D), meshEX, (0,0,1))[0]              #3D End Point
        self.drop = self.start.Z - self.end.Z                 #Elevation Drop across length of curve
        self.points2D = rs.DivideCurveLength(self.Thalweg2D, self.lenDivision, True, True) #Divide curve into lengths X (,X,,)
        self.points3D = []
        
        #Need to Project Points to Mesh one by one. When projecting all points to mesh, 
        #they slowly diverge in X and Y values from the original 2D points, therefore 
        #projcting to a different Z value 
        for i in self.points2D:
            self.points3D.append(rs.ProjectPointToMesh(i, meshEX, (0,0,1))[0])

        #Set up Riffles
        self.createRiffles(meshEX)
        
        #Get Bank Points
        self.setBankInfo(meshEX)
        
        #get existing conditions values
        #?????Should we do this after the getIdealRiffleDesign so that we can vary the window
        #?????based on the ideal riffle length? Answer: No. Ideal Riffle Design Requires Valley Slope.
        self.getSlopes(2,5)                #(,X) X is important and factors into variances alot. Need to not hard code in.
        self.getIdealRiffleDesign(.5, 10, meshEX)
        self.getBendRatios(5)
        self.getCurvature(5)

        #*****************************************
        #can now link this to the design iterator (justin) for riffle width and depth, using bank width as the riffle
        #width and plugging in a flowrate. 
        #*****************************************


    def createRiffles(self, meshEX):
        for i in range(len(self.points2D)):
            self.riffles.append(StreamPoint(self.points3D[i], self.Thalweg2D, i, self.lenDivision, meshEX))
        return

    def setBankInfo(self, meshEX):
        
        for i in self.riffles:
            #Bank Points
            i.ptBankRight = rs.ProjectPointToMesh(rs.EvaluateCurve(self.BankRight2D, rs.CurveClosestPoint(self.BankRight2D, self.points2D[i.index])), meshEX, (0,0,1))[0]
            i.ptBankLeft = rs.ProjectPointToMesh(rs.EvaluateCurve(self.BankLeft2D, rs.CurveClosestPoint(self.BankLeft2D, self.points2D[i.index])), meshEX, (0,0,1))[0]
            i.elevBankLow = min(i.ptBankLeft.Z, i.ptBankRight.Z)
            
            #others
            i.bank_width = horizontal_distance(i.ptBankRight, i.ptBankLeft)
            #Bank width and elevBankLow are coming out the same for 2-5 in a row??? I believe this is because the nearest bank points are the same for those 2-5 points.

            i.BankRightIncision = i.ptBankRight.Z - i.invertChannel.Z 
            i.BankLeftIncision = i.ptBankLeft.Z - i.invertChannel.Z 
            i.ptBankMin = rs.coerce3dpoint((i.invertChannel.X, i.invertChannel.Y, i.elevBankLow))
        
        return

    def getSlopes(self, winChannel, winValley):
        #getSlopes defines the *discrete* slopes of the line, based on the straight distance between points2D on the line
        
        #Channel Slope
        for i in range(len(self.riffles)):
            t1 = min([i, winChannel])
            t2 = min([len(self.riffles)-i-1, winChannel])
            sta1 = self.riffles[i - t1].station
            sta2 = self.riffles[i + t2].station
            pt1_z = self.riffles[i - t1].ptBankMin.Z
            pt2_z = self.riffles[i + t2].ptBankMin.Z
            self.riffles[i].channel_slope = (pt1_z - pt2_z)/(sta1 - sta2)
                   

        #Valley Slope
        for i in range(len(self.riffles)): 
            t1 = min([i, winValley])
            t2 = min([len(self.riffles)-i-1, winValley])
            sta1 = self.riffles[i - t1].station
            sta2 = self.riffles[i + t2].station
            pt1_z = self.riffles[i - t1].elevBankLow
            pt2_z = self.riffles[i + t2].elevBankLow
            self.riffles[i].valley_slope = (pt1_z - pt2_z)/(sta1 - sta2)
        return

    def getIdealRiffleDesign(self, riffle_drop_min, riffle_length_min, meshEX): 
        ##need an additional variable - that is able to be reset

        #Setup Variables
        cl = self.Thalweg2D
        crvBR = self.BankRight2D
        crvBL = self.BankLeft2D

        points = []
        interval = 0.2 * self.lenDivision

        #split curve into 0.1 increments to be sampled
        points2D = rs.DivideCurveLength(cl, interval, True, True)
        


        #Project points to mesh creates a different array than Ppoints2D. Not sure how/why, but 
        #need to loop through in method below to keep remaining code reading array correctly
        for i in points2D:
             #?There has to be a better way to do this
            #ptBR = rs.EvaluateCurve(crvBR, rs.CurveClosestPoint(crvBR, i))
            #ptBL = rs.EvaluateCurve(crvBL, rs.CurveClosestPoint(crvBL, i))
            
            ptBR = rs.ProjectPointToMesh(rs.EvaluateCurve(crvBR, rs.CurveClosestPoint(crvBR, i)), meshEX, (0,0,1))[0]
            ptBL = rs.ProjectPointToMesh(rs.EvaluateCurve(crvBL, rs.CurveClosestPoint(crvBL, i)), meshEX, (0,0,1))[0]
            elevBankLow = min(ptBR.Z, ptBL.Z)
            points.append(rs.coerce3dpoint((i.X, i.Y, elevBankLow)))
            


            
        #Calculate Ideal riffle design for each stream point
        for i in self.riffles:
            
            #Set initial riffle sizes
            check = False
            count = 0
            riffle_drop = riffle_drop_min       #Initial drop test
            riffle_length = riffle_length_min   #Initial length test

            print("************************")
            print("New Riffle", i.station, len(points), round(self.end.Z,2))


            #loop through sizing scenarios
            while check == False and count < 35:
                
                #Set initial Values
                i.riffle.pt_start = i.ptBankMin
                rUSInvert = i.ptBankMin.Z
                rDSInvert = rUSInvert - riffle_drop
                pool_station_start = i.station + riffle_length

                #Check that rDSInvert is not lower than thalweg2D endpoint
                if rDSInvert < self.end.Z:
                    i.use = 0
                    print(i.station, "Lower than end point")
                    break   #breaks the "While" Loop
                

                #Calc Pool length by when it gets to next point on centerline at same elevation
                #Get index for starting point
                iStartPoint = int(round(pool_station_start, 1) / interval)

                print('Find Elevation')
                print("Count: ", count)
                print("Station: ", i.station)
                print("X: ", round(i.ptBankMin.X, 2),"Y: ", round(i.ptBankMin.Y, 2), "Z: ", round(i.ptBankMin.Z, 2))
                print("Start Point: ", iStartPoint)
                print("X: ", round(points[int(i.station / interval)].X, 2),"Y: ", round(points[int(i.station / interval)].Y, 2), "Z: ", round(points[int(i.station / interval)].Z, 2))


                #Find Downstream point j where rDSInvert is higher than channel
                #this means that the interval has to be low enough to catch an approximate elevation
                #where the pool will meet the channel
                #?Can this be changed to automatically find the point at that elevation beyond a certain length?
                for j in range(iStartPoint, len(points)):
                    #print("1-----", j, round(points[j-10].Z, 2), round(points[j].Z, 2), round(rDSInvert, 2))
                    if points[j].Z <= rDSInvert:
                        pool_length = (j-1) * interval - pool_station_start
                        pt = points[j]
                        #print ("2-----", j, i.station, pool_station_start, pool_length, round(points[j].Z, 2))
                        break   #breaks the "for" loop
                    #print("iteration", j, pool_length, i.station, pool_station_start, points[j].Z)
                        

                #Changes 
                if pool_length >= 1.5 * riffle_length:
                    i.geometry = "Riffle"
                    i.riffle.length = riffle_length
                    i.riffle.length_max = riffle_length
                    i.riffle.length_min = 1.5 * riffle_length
                    i.riffle.drop = riffle_drop
                    i.riffle.slope = riffle_drop / riffle_length
                    i.riffle.station_end = i.station + i.riffle.length
                    
                    i.pool.length = pool_length
                    i.pool.station_start = i.riffle.station_end
                    i.pool.station_end = i.station + i.riffle.length + i.pool.length
                    check = True
                else:
                    if riffle_length < 30:
                        riffle_length += 5
                        count +=1
                    elif riffle_drop < 2:
                        riffle_length = riffle_length_min
                        riffle_drop += 0.25
                        count +=1
                    else:
                        i.geometry = "Neither"
                        #print(i.station, "geometry=", i.geometry)
                        check = True
                    #!!!NEED TO ADD IN CASCADE
            #print("here", i.station, i.geometry, riffle_length, pool_length)
        return



    def getCurvature(self, t):
        for i in range(1 , len(self.riffles)):#-t): ?Don't think we need to subtract last "t" as with getBendRatios
            print(self.riffles[i].station, self.riffles[i].parameter, self.riffles[i].curvature)
            print(self.Thalweg2D)
            self.riffles[i].curvature = rs.CurveCurvature(self.Thalweg2D, self.riffles[i].parameter)[3]
            print(self.riffles[i].curvature)
        return
        
    def getBendRatios(self, t):
        array_bend_ratio = []

        #get first list of bend_ratios
        for i in range(len(self.riffles)-t):
      
            p = horizontal_distance(self.riffles[i].ptBankLeft, self.riffles[i+t].ptBankLeft)
            l = abs(self.riffles[i].station - self.riffles[i+t].station)
            p_diff = abs(p - l)
            
            self.riffles[i].bend_ratio = p_diff
            array_bend_ratio.append(p_diff)

        #Normalize
        old_min = min(array_bend_ratio)
        old_range = max(array_bend_ratio) - old_min
        
        new_min = 0
        new_range = 1 - new_min

        for i in range(len(self.points2D)-t):
            n = self.riffles[i].bend_ratio
            new_bend_ratio = (n - old_min) / old_range * new_range + new_min
            self.riffles[i].bend_ratio = new_bend_ratio

        return
    
class StreamPoint(object):
    """docstring for ClassName"""
    #Notes to think about:
    # -Does difference in left/right bank elevation matter in design?

    def __init__(self, point, crvCenterline, index, lenDivision, meshEX):
        #Define Initial Values
        #self.pt = point
        self.index = index
        self.station = index * lenDivision
        
        #Thalweg2D Information 
        self.parameter = rs.CurveClosestPoint(crvCenterline, point)     #Parameter (t) for point on centerline
        self.tangent = rs.CurveTangent(crvCenterline, self.parameter)
        self.slopeAtPoint = self.tangent[2] #??This won't work anymore with flat thalweg
        self.bend_ratio = None
        self.curvature = None
        
        #Thalweg3D Information
        self.invertChannel = point
        self.channel_slope = None
        self.valley_slope = None
        

        #Bank Information
        self.ptBankRight = None 
        self.ptBankLeft = None 
        self.elevBankLow = None
        self.ptBankMin = None
        self.bank_width = None
        self.BankRightIncision = None
        self.BankLeftIncision = None
        self.incision = None

        #Use
        self.suitability = 0
        self.use = None                    #1 = Riffle, 0 = Don't Use, -1 = Pool (pool points2D not usedd for now)
        
        #Proposed Riffle Design Information
        self.riffle = RifflePoint()
        self.pool = PoolPoint()
        self.geometry = None
        
        #project Thalweg2D to Horizontal Plane
        crvCenterlineHoriz = rs.CopyObject(crvCenterline)
        rs.ScaleObject(crvCenterlineHoriz, (0,0,0), (1,1,0))
        self.parameterHorizontal = rs.CurveClosestPoint(crvCenterlineHoriz, point)
 
class RifflePoint(object):
    
    def __init__(self):
        #Proposed Riffle Design Information
        self.length = None
        self.drop = None
        self.width = None     #Calc based on Bank Width
        self.depth = None
        self.station_start = None 
        self.station_end = None
        self.pt_start = None
        self.pt_end= None
    
class PoolPoint(object):

    def __init__(self):
        #Proposed Riffle Design Information
        self.length = None
        self.length_min = None
        self.length_max = None
        self.slope = None
        self.drop = None
        self.width = None     #Calc based on Bank Width
        self.station_start = None
        self.station_end = None
        self.pt_start = None
        self.pt_end= None
               
def horizontal_distance(pt1, pt2):
    distance = math.sqrt(math.pow(pt2.X - pt1.X, 2) + math.pow(pt2.Y - pt1.Y, 2)) 
    return distance

#x Channel is set as curve in centerline class
crvRifflePoints = Centerline(crvThalweg2D, Mesh, crvRightBank, crvLeftBank, interval)

for i in crvRifflePoints.riffles:
    print(i.station, i.geometry)  