import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 
import time

#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy


class Centerline(object):
    def __init__(self, crvCenterline, meshEX, crvBankRight, crvBankLeft, lenDivision):

        #Centerline information
        self.Thalweg2D = crvCenterline
        self.BankRight2D = crvBankRight
        self.BankLeft2D = crvBankLeft
        self.lenDivision = lenDivision
        self.length = rs.CurveLength(self.Thalweg2D)             
        self.start = getPointFromMesh_Thalweg(self.Thalweg2D, 0, meshEX)
        self.end = getPointFromMesh_Thalweg(self.Thalweg2D, rs.CurveLength(self.Thalweg2D), meshEX)
        self.drop = self.start.Z - self.end.Z                 
        self.points2D = rs.DivideCurveLength(self.Thalweg2D, self.lenDivision, True, True) 
        self.points3D = []
        for i in self.points2D:
            self.points3D.append(rs.ProjectPointToMesh(i, meshEX, (0,0,1))[0])
            #Need to Project Points to Mesh one by one. When projecting all points to mesh, 
            #they slowly diverge in X and Y values from the original 2D points, therefore 
            #projecting to a different Z value. This appears to be slow. 
        
        #???Check for the "hiccups in projection. They appear to only be in single points and can be smoothed. Always appear to be lower than others nearby. Only checks for lower currently. Ideally, we don't have to do this.
        for i in range(1, len(self.points3D)-1):
            zR1 = self.points3D[i-1].Z
            zR2 = self.points3D[i+1].Z
            if self.points3D[i].Z < zR1 and self.points3D[i].Z < zR2:
                self.points3D[i].Z = (zR1+zR2)/2


        time_step1 = time.time()

        #Set up Riffles
        self.riffles = []      
        self.createRiffles(meshEX)
        
        time_step2 = time.time()

        #Get Bank Points
        self.setBankInfo(meshEX)
        
        time_step3 = time.time()

        #get existing conditions values
        #(,X) X is important and factors into variances alot. Need to not hard code in.
        self.getSlopes(2,5)       
        
        time_step4 = time.time()

        self.getIdealRiffleDesign(.5, 10, meshEX)
        
        time_step5 = time.time()

        self.getBendRatios(5)
        
        time_step6 = time.time()

        self.getCurvature(5)
        
        time_step7 = time.time()

        print('Step 1 Comp Time:', time_step1-time_start)
        print('Step 2 Comp Time:', time_step2-time_start)
        print('Step 3 Comp Time:', time_step3-time_start)
        print('Step 4 Comp Time:', time_step4-time_start)
        print('Step 5 Comp Time:', time_step5-time_start)
        print('Step 6 Comp Time:', time_step6-time_start)
        print('Step 7 Comp Time:', time_step7-time_start)


        #*****************************************
        #can now link this to the design iterator (justin) for riffle width and depth, using bank width as the riffle
        #width and plugging in a flowrate. 
        #*****************************************

    def createRiffles(self, meshEX):
        for i in range(len(self.points3D)):
            self.riffles.append(StreamPoint(self.points3D[i], self.Thalweg2D, i, self.lenDivision))
        return

    def setBankInfo(self, meshEX):
        
        for i in self.riffles:

            #Bank Points
            i.ptBankRight = getPointFromMesh_Bank(self.Thalweg2D, self.BankRight2D, i.station, meshEX)
            i.ptBankLeft = getPointFromMesh_Bank(self.Thalweg2D, self.BankLeft2D, i.station, meshEX)
        
        #???Check for the "hiccups in projection. They appear to only be in single points and can be smoothed. Always appear to be lower than others nearby. Only checks for lower currently. Ideally, we don't have to do this.
        for i in range(1, len(self.riffles)-1):
            #Right Bank
            zR1 = self.riffles[i-1].ptBankRight.Z
            zR2 = self.riffles[i+1].ptBankRight.Z
            if self.riffles[i].ptBankRight.Z < zR1 and self.riffles[i].ptBankRight.Z < zR2:
                self.riffles[i].ptBankRight.Z = (zR1+zR2)/2

            #Left Bank
            zR1 = self.riffles[i-1].ptBankLeft.Z
            zR2 = self.riffles[i+1].ptBankLeft.Z
            if self.riffles[i].ptBankLeft.Z < zR1 and self.riffles[i].ptBankLeft.Z < zR2:
                self.riffles[i].ptBankLeft.Z = (zR1+zR2)/2

        for i in self.riffles:

            #Bank Points
            i.elevBankLow = min(i.ptBankLeft.Z, i.ptBankRight.Z)
            
            #others
            i.bank_width = horizontal_distance(i.ptBankRight, i.ptBankLeft)
            #??Bank width and elevBankLow are coming out the same for 2-5 in a row??? I believe this
            #??is because the nearest bank points are the same for those 2-5 points.

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
        
        #Inital riffle set up info    
        for i in self.riffles:
            i.riffle.pt_start = i.ptBankMin
            i.riffle.width = 10 #i.bank_width

        #Calculate Ideal riffle design for each stream point
        for i in self.riffles:
            
            #Set initial riffle sizes
            count = 0
            i.riffle.drop = riffle_drop_min         #Initial drop test
            i.riffle.length = riffle_length_min     #Initial length test

            print("************************")
            print("New Riffle", i.station, len(self.riffles), round(self.end.Z,2))


            #Iterate through riffles sizes
            while count < 35:
                
                #Set initial riffle/pool Values
                i.pool.station_start = i.station + i.riffle.length
                
                #set additional temp values
                rDSInvert = i.riffle.pt_start.Z - i.riffle.drop


                #Check that rDSInvert is not lower than centerline endpoint
                if rDSInvert < self.end.Z:
                    i.use = 0
                    print(i.station, ' is lower than the stream end point')
                    break   #breaks the "While" Loop
                

                #Calc Pool length by when it gets to next point on centerline at same elevation
                print('Find Elevation')
                print("Count: ", count)
                print("Riffle Start Point: ", i.station)
                print("X: ", round(i.ptBankMin.X, 2),"Y: ", round(i.ptBankMin.Y, 2), "Z: ", round(i.ptBankMin.Z, 2))
                print("Pool Start Point: ", i.pool.station_start, 'pool elevation:', rDSInvert)


                #Find Downstream point j where rDSInvert is higher than channel
                #this means that the interval has to be low enough to catch an approximate elevation
                #where the pool will meet the channel
                #????Can this be changed to automatically find the point at that elevation beyond a certain length?
                for j in self.riffles[int(i.riffle.station_start/self.lenDivision) + 1:len(self.riffles)]:
                    
                    print("1-----", j.index, round(rDSInvert, 2), round(j.riffle.pt_start.Z, 2))
                    if j.riffle.pt_start.Z <= rDSInvert:
                        i.pool.station_end = j.riffle.station_start
                        i.pool.length = i.pool.station_end - i.pool.station_start
                        i.pool.pt_end = j.riffle.pt_start
        
                        print ("2-----", j, i.station, i.pool.station_start, i.pool.length, round(j.riffle.pt_start.Z, 2))
                        break                         

                #--------------Iterate through riffle sizes ---------------------------------------------


                if i.pool.length >= 1.5 * i.riffle.length:
                    #Current sizes meet criteria. Set remaining riffle/pool info
                    i.geometry = "Riffle"
                    i.riffle.slope = i.riffle.drop / i.riffle.length
                    i.riffle.station_end = i.station + i.riffle.length
                    i.pool.index = int(i.riffle.station_end/self.lenDivision)
                    rEnd = self.riffles[i.pool.index]
                    pEnd = self.riffles[int(i.pool.station_end/self.lenDivision)]
                    i.riffle.tangent_end = rEnd.tangent
                    i.pool.tangent_start = rEnd.tangent
                    i.pool.tangent_end = pEnd.tangent
                    i.riffle.pt_end = rs.coerce3dpoint((rEnd.riffle.pt_start.X, rEnd.riffle.pt_start.Y, rDSInvert))
                    i.pool.pt_start = i.riffle.pt_end  
                    break

                else:
                    #Iterate through riffle drop first
                    if i.riffle.drop < 2:
                        i.riffle.drop += 0.25
                        count +=1
                    #then iterate length and reset the riffle drop
                    elif i.riffle.length < 30:
                        i.riffle.drop = riffle_drop_min
                        i.riffle.length += 5
                        count +=1
                    #maxes out on riffle iterations, need to add cascade values. 
                    else:
                        i.geometry = "Neither"
                        #print(i.station, "geometry=", i.geometry)
                        break
                    #????NEED TO ADD IN CASCADE
        return

    def getCurvature(self, t):
        
        curves = []

        for i in range(0 , len(self.riffles)):
            print(self.riffles[i].station, self.riffles[i].parameter, self.riffles[i].curvature)
            curves.append(rs.CurveCurvature(self.Thalweg2D, self.riffles[i].parameter)[3])
            print(curves[i])


        #This is going to be averaging as it goes through
        for i in range(1 , len(self.riffles)-10):
            curvature  = 0
            count = 0   
            for j in range(i, i + 10):
                curvature += curves[i]
                count += 1
            self.riffles[i].curvature = curvature / count

        for i in range(len(self.riffles)-10, len(self.riffles)):
            self.riffles[i].curvature = curves[i]

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

        #Normalize - ?? Need to update normalization. Should we have this be a separate function?
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

    def __init__(self, point, crvCenterline, index, lenDivision):
        #Define Initial Values
        #self.pt = point
        self.index = index
        self.station = index * lenDivision
        
        #Thalweg2D Information 
        self.parameter = rs.CurveClosestPoint(crvCenterline, point)     #2D Parameter (t) for point on centerline
        self.tangent = rs.CurveTangent(crvCenterline, self.parameter)   #2D Tangent
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
        self.use = None                    #2 = Gap in riffle/pool, 1 = Riffle, 0 = Don't Use, -1 = Pool (pool points2D not usedd for now)
        
        #Proposed Riffle Design Information
        self.geometry = None
        self.riffle = RifflePoint()
        self.riffle.index = self.index
        self.riffle.station_start = self.station

        self.pool = PoolPoint()
 
class RifflePoint(object):
    
    def __init__(self):
        #Proposed Riffle Design Information
        self.index = None
        self.length = None
        self.drop = None
        self.width = None     #Calc based on Bank Width
        self.depth = None
        self.station_start = None 
        self.station_end = None
        self.pt_start = None
        self.pt_end= None
        self.tangent_end = None
    
class PoolPoint(object):

    def __init__(self):
        #Proposed Riffle Design Information
        self.index = None
        self.length = None
        self.length_min = None
        self.length_max = None
        self.slope = None
        self.drop = None
        self.width = None     #Calc based on Bank Width
        self.depth = None
        self.station_start = None
        self.station_end = None
        self.pt_start = None
        self.pt_end= None
        self.tangent_start = None
        self.tangent_end = None
         
def getPointFromMesh_Bank(cl, crvBank, station, mesh):
    
    if station == 0:
        pt2D_cl = rs.CurveStartPoint(cl)
    else: 
        pt2D_cl = rs.DivideCurveLength(cl, station, True, True)[1]    
    
    t = rs.CurveClosestPoint(crvBank, pt2D_cl)
    pt2D = rs.EvaluateCurve(crvBank, t)
    pt3D = rs.ProjectPointToMesh(pt2D, mesh, (0,0,1))[0]

    return pt3D

def getPointFromMesh_Thalweg(cl, station, mesh):

    if station == 0:
        pt2D = rs.CurveStartPoint(cl)
    else: 
        pt2D = rs.DivideCurveLength(cl, station, True, True)[1]    

    pt3D = rs.ProjectPointToMesh(pt2D, mesh, (0,0,1))[0]
    print(pt2D, pt3D)
    return pt3D

def horizontal_distance(pt1, pt2):
    distance = math.sqrt(math.pow(pt2.X - pt1.X, 2) + math.pow(pt2.Y - pt1.Y, 2)) 
    return distance

def printriffledata(riffle):

    print(riffle.geometry)
    
    if riffle.geometry=='Neither':
        return

    #Print Riffle info
    print('riffle index:', riffle.riffle.index)
    print('riffle length:', riffle.riffle.length)
    print('riffle drop:', riffle.riffle.drop)
    print('riffle width:', riffle.riffle.width)
    print('riffle depth:', riffle.riffle.depth)
    print('riffle station start:', riffle.riffle.station_start)
    print('riffle station end:', riffle.riffle.station_end)
    print('riffle pt start:', riffle.riffle.pt_start)
    print('riffle pt start z:', riffle.riffle.pt_start.Z)
    print('riffle pt end:', riffle.riffle.pt_end)
    print('riffle pt end z:', riffle.riffle.pt_end.Z)

    #print pool info
    print('pool index:', riffle.pool.index)
    print('pool length:', riffle.pool.length)
    print('pool slope:', riffle.pool.slope)
    print('pool drop:', riffle.pool.drop)
    print('pool width:', riffle.pool.width)
    print('pool station start:', riffle.pool.station_start)
    print('pool station end:', riffle.pool.station_end)
    print('pool pt start:', riffle.pool.pt_start)
    print('pool pt start z:', riffle.pool.pt_start.Z)
    print('pool pt end:', riffle.pool.pt_end)
    print('pool pt end z:', riffle.pool.pt_end.Z)


time_start = time.time()
print('Comp Time:', time_start-time_start)

#x Channel is set as curve in centerline class
crvRifflePoints = Centerline(crvThalweg2D, Mesh, crvRightBank, crvLeftBank, interval)

for i in crvRifflePoints.riffles:
    print(i.station, i.geometry)  

