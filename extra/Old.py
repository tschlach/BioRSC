Old


def find_Gaps(cl, iCurrent):
    #cl:  centerline class
    #iCurrent: index of current riffle  
    iUS = None              #index of Upstream riffle already flagged
    iDS = None              #index of Downstream riffle already flagged
    gapUS = None
    gapDS = None

    print('find_Gaps, iCurrent=', iCurrent)
    #FIND UPSTREAM RIFFLE
    #NOTE: THIS SEARCHES ALL THE WAY TO THE BEGINNING. ONLY NEED TO SEARCH WITHIN SELECT RANGE ?????
    for i in range(iCurrent-1, 0, -1):
        # print('fg i=', i)
        if cl.riffles[i].use == 0:
            iUS = i
            gapUS = cl.riffles[iCurrent].station - cl.riffles[i].pool.station_end  
            # print('1fg iDS, gapDS=', iDS, gapDS)

    #FIND DOWNSTREAM RIFFLE
    #NOTE: THIS SEARCHES ALL THE WAY TO THE BEGINNING. ONLY NEED TO SEARCH WITHIN SELECT RANGE ?????
    for i in range(iCurrent + 1, len(cl.riffles), 1):
        if cl.riffles[i].use == 1:
            iDS = i
            gapDS = cl.riffles[i].station - cl.riffles[iCurrent].pool.station_end

    print('2fg iDS, gapDS=', iDS, gapDS)
    return iUS, gapUS, iDS, gapDS

    
def get_RiffleTiers(list_values):

    #Filter 1
    for i in range(len(list_values)):
        if list_values[i][12] == "Riffle":                   #Geometry Check
            if list_values[i][2] > 10:                       #Bend_ratio Check (value random, need to select)
                TierR1.append(list_values[i])
            elif list_values[i][2] > 5:
                TierR2.append(list_values[i])
            else:
                TierR3.append(list_values[i])
        elif list_values[i][12] == "Pool":                   #Geometry Check
            TierP1.append(list_values[i])
        else:
            TierNull.append(list_values[i])
    return 

def delete_Riffles(iLower, iUpper):
    #iLower, iUpper are Stations within Tier classes

    print("----------")
    print("Delete Riffles")
    print("Total Count=", len(listVariables), 'Final Station=', listVariables[-1][1])
    print('R1 Count=', len(TierR1))

    #Tried to make a separate function but it didn't work. Should come back to it.
    i=0
    while i < len(TierR1):
        print("----------")
        print(len(TierR1))
        print('i=', i)
        print(TierR1[i][1])
        if iLower <= TierR1[i][1] < iUpper:
            print('Delete:',TierR1[i][1], TierR1[i][0], TierR1[i])
            TierR1.remove(TierR1[i])                #
            print(len(TierR1))
            print('i=', i)
        else:
            i += 1

    i = 0
    while i < len(TierR2):
        print("----------")
        print(len(TierR2))
        print('i=', i)
        print(TierR2[i][1])
        if iLower <= TierR2[i][1] < iUpper:
            print('Delete:',TierR2[i][1], TierR2[i][0], TierR2[i])
            TierR2.remove(TierR2[i])                
            print(len(TierR2))
            print('i=', i)
        else:
            i += 1
    i = 0
    while i < len(TierR3):
        print("----------")
        print(len(TierR3))
        print('i=', i)
        print(TierR3[i][1])
        if iLower <= TierR3[i][1] < iUpper:
            print('Delete:',TierR3[i][1], TierR3[i][0], TierR3[i])
            TierR3.remove(TierR3[i])                
            print(len(TierR3))
            print('i=', i)
        else:
            i += 1

    print('R1 Count=', len(TierR1))
    print("End Delete Riffles")
    print("----------")
    retur

def find_NextDSRiffle(l, t, targetSTA, targetElev):
    #targetSTA = station of end of pool based on station of current riffle, length
    #            of riffle, and length of pool
    #targetElev = Elevation of current riffle - drop of current riffle

    print('target:', targetSTA, targetElev)
    for i in range(t, len(l)):
        rNext = l[i]

        print(rNext[1], rNext[13])

        #Check length from previous
        if rNext[1] >= targetSTA: 
            #Check that invert is within 0.1ft of target invert
            if abs(rNext[13]-targetElev) < 0.1:
                index = rNext[0]
                return index, i
    return None, i

def find_NextUSRiffle(l, t, targetSTA, targetElev):
    #targetSTA = Station of current Riffle
    #targetElev = Elevation of current riffle

    print('t = ', t)
    print('target:', targetSTA, targetElev)

    #Loop Through upstream Riffles
    for i in range(t-1, 0, -1):       #could try reversed(range()), may be faster
        
        #gets next US Riffle
        rNext = l[i]

        #Consider just making this a variable of the riffle (targetSTA)
        #rNext_EndStation = rSTA + rL + pL
        rNext_EndStation = rNext[1] + rNext[8] + rNext[8] 
        
        #rNext_EndElev = Elevation - Drop
        rNext_EndElev = rNext[13] - rNext[10]

        print(rNext[1], rNext[13], rNext[10], rNext_EndStation, rNext_EndElev)

        #End of Pool for US Riffle needs to be before targetSTA
        if rNext_EndStation <= targetSTA: 
            #Check that invert is within 0.1ft of target invert
            if abs(rNext_EndElev-targetElev) <= 0.1:
                index = rNext[0]
                return index, i
    return None, Non

def get_VariableArray(centerline):

    w, h = 14, len(centerline.riffles)
    list_values = [[None] * w for i in range(h)]
        
    c = 0
    # print(list_values)
 
    for i in centerline.riffles:     #i = RifflePoint Class feature

        list_values[c][0] = i.index
        list_values[c][1] = i.station 
        list_values[c][2] = i.bend_ratio2  #i.bend_ratio
        list_values[c][3] = i.bank_width
        list_values[c][4] = i.BankRightIncision
        list_values[c][5] = i.BankLeftIncision
        list_values[c][6] = i.elevBankLow
        list_values[c][7] = i.valley_slope
        list_values[c][8] = i.riffle.length
        list_values[c][9] = i.riffle.slope
        list_values[c][10] = i.riffle.drop
        list_values[c][11] = i.riffle.width
        list_values[c][12] = i.geometry
        list_values[c][13] = i.pt.Z 
        # list_values[c][x] = 
        # list_values[c][x] = i.parameter
        # list_values[c][x] = i.tangent
        # list_values[c][x] = i.slopeAtPoint
        # list_values[c][x] = i.channel_slope
        # list_values[c][x] = i.valley_slope
        # list_values[c][x] = i.pt
        # list_values[c][x] = i.ptBankRight
        # list_values[c][x] = i.ptBankLeft 

        c += 1
   
    return  list_value

    #Append to final List
        # list_Final.append(listAll[iLM_Max])

        # #get riffle/pool length
        # rCurrent = centerline.riffles[iLM_Max]
        # rSTA = rCurrent.station
        # print_RiffleInfo(rCurrent, iLM_Max)

        # #delete from Tier
        # TierR1.remove(TierR1[iTier_Max])

        #++++++++++++++++++++++++++++++++++++++++++++++
        #Search 2
        #++++++++++++++++++++++++++++++++++++++++++++++
        #assume pool length = riffle length
        #this will need to be adjusted later more intelligently

        #Loop Through
        #Look downstream at next value distance down of riffle and pool length from last
        #find station nearest to end of US riffle
        # print("Looking Downstream")

        # targetSTA = rCurrent.station + rCurrent.riffle_length + rCurrent.riffle_length
        # targetElev = rCurrent.pt.Z - rCurrent.riffle_drop
        # t = iTier_Max
        
        # removeLowerLimit = rSTA
        # removeUpperLimit = targetSTA

        # while t < len(TierR1):
        #     print(t)
        #     iLM_Next, t = find_NextDSRiffle(TierR1, t, targetSTA, targetElev)
        #     print(t)

        #     if iLM_Next != None:

        #         list_Final.append(listAll[iLM_Next])
        #         rCurrent = centerline.riffles[iLM_Next]
        #         targetSTA = rCurrent.station + rCurrent.riffle_length + rCurrent.riffle_length
        #         targetElev = rCurrent.pt.Z - rCurrent.riffle_drop
        #         removeUpperLimit = targetSTA
        #         print_RiffleInfo(rCurrent, iLM_Next)
        #     else:
        #         t = len(TierR1)

        # print("Lower Limit=", removeLowerLimit, '; Upper Limit=', removeUpperLimit)
        
        # delete_Riffles(removeLowerLimit, removeUpperLimit)

        # #Loop Through
        # '''
        # Look upstream at next value distance down of riffle and pool length from last
        # If yes
        #     #add to final list
        #     #delete from tier
        # if no, set up loop to look in either direction by a specific amount
        # '''

        # #Reset i to original value from first Riffle
        # #get riffle/pool length of first riffle
        # rCurrent = centerline.riffles[iLM_Max]
        # targetSTA = rCurrent.station 
        # targetElev = rCurrent.pt.Z 
        # print("Looking Upstream")
        # t = iTier_Max
        
        # removeUpperLimit = targetSTA 

        # while t > 0:
        #     print(t)
        #     iLM_Next, t = find_NextUSRiffle(TierR1, t, targetSTA, targetElev)
        #     print(t)
            
        #     if iLM_Next != None:
        #         list_Final.append(listAll[iLM_Next])
        #         rCurrent = centerline.riffles[iLM_Next]
        #         targetSTA = rCurrent.station 
        #         targetElev = rCurrent.pt.Z
        #         removeLowerLimit = targetSTA 
        #         print_RiffleInfo(rCurrent, iLM_Next)
        #     else:
        #         t = 0          

        # test +=1
                
        # print("Lower Limit=", removeLowerLimit, '; Upper Limit=', removeUpperLimit)
        
        # delete_Riffles(removeLowerLimit, removeUpperLimit)


        # print("----------")
        # print("TierR1, length=", len(TierR1))
        # #print(TierR1)
        # print("----------")

    # print(TierR1)

    import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 
#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy

#x = Thalweg
#y = Division lengths for points along centerline
#z = Right Bank 
#u = Left Bank


class Centerline(object):
    def __init__(self, crvCenterline, crvBankRight, crvBankLeft, lenDivision):
        #****makes a list of each variable. In order, but not attributed to each point. 
        #****may want to pull everything under point info
        self.Thalweg = crvCenterline
        self.lenDivision = lenDivision
        self.BankRight = crvBankRight
        self.BankLeft = crvBankLeft
        self.length = rs.CurveLength(crvCenterline)             #Length
        self.start = rs.CurveStartPoint(crvCenterline)          #3D Start Point
        self.end = rs.CurveEndPoint(crvCenterline)              #3D End Point
        self.drop = self.start[2] - self.end[2]                 #Elevation Drop across length of curve
        self.points = rs.DivideCurveLength(crvCenterline, lenDivision, True, True) #Divide curve into lengths X (,X,,)
        self.riffles = []      

        #Set up Riffles
        self.createRiffles(lenDivision)
        
        #get existing conditions values
        #?????Should we do this after the getIdealRiffleDesign so that we can vary the window
        #?????based on the ideal riffle length? Answer: No. Ideal Riffle Design Requires Valley Slope.
        self.getSlopes(2,5)                #(,X) X is important and factors into variances alot. Need to not hard code in.
        self.getIdealRiffleDesign(.5, 10)
        self.getBendRatios(5)
        self.getBendRatios2(5)

        #calculate deisgn values
        
        
        #*****************************************
        #can now link this to the design iterator (justin) for riffle width and depth, using bank width as the riffle
        #width and plugging in a flowrate. 
        #*****************************************


     
        #Error handling/Print Values
        # for i in range(len(self.points)):
        #     print(self.riffles[i].station)
            # print(self.riffles[i].bend_ratio)
        #     print(self.riffles[i].slopeAtPoint)
        #     print(self.riffles[i].bank_width)
        #     print(self.riffles[i].pt)
        #     print(self.riffles[i].ptBankRight)
        #     print(self.riffles[i].ptBankLeft)
        #     print("----------")
        
    def getIdealRiffleDesign(self, riffle_drop_min, riffle_length_min): 
        ##need an additional variable - that is able to be reset

        #Calculate Ideal riffle design for each stream point
        for i in self.riffles:
            check = False
            count = 0
            riffle_drop_test = riffle_drop_min
            riffle_length_test = riffle_length_min
            
            #loop through sizing scenarios
            while check == False and count < 35:
                
                print('channel slope;', i.channel_slope)
                if i.channel_slope == 0: 
                    pool_length = 10000
                else:  
                    pool_length = abs((riffle_drop_test / i.channel_slope) - riffle_length_test)

                print('STA=', i.station, '; Valley Slope=', i.channel_slope, '; PL=', pool_length, '; rLt=', riffle_length_test, '; rDt=', riffle_drop_test)
                if pool_length >= riffle_length_test:
                    i.geometry = "Riffle"
                    i.riffle.length = riffle_length_test
                    i.riffle.drop = riffle_drop_test
                    i.riffle.slope = riffle_drop_test / riffle_length_test
                    i.riffle.station_end = i.station + i.riffle.length
                    
                    #!!!This need to be adjusted, was only in because bad LiDAR
                    if pool_length == 10000:
                        i.pool.length = i.riffle.length
                    else:
                        i.pool.length = pool_length
                    i.pool.station_start = i.riffle.station_end
                    i.pool.station_end = i.station + i.riffle.length + i.pool.length
                    check = True
                else:
                    if riffle_length_test < 30:
                        riffle_length_test += 5
                        count +=1
                    elif riffle_drop_test < 2:
                        riffle_length_test = riffle_length_min
                        riffle_drop_test += 0.25
                        count +=1
                    else:
                        i.geometry = "Neither"
                        check = True
        return

    def createRiffles(self, lenDivision):
        for i in range(len(self.points)):
            station = i * lenDivision
            self.riffles.append(StreamPoint(self.points[i], self.Thalweg, self.BankRight, self.BankLeft, station, lenDivision))
        return
    
    def getBendRatios2(self, t):
        for i in range(len(self.riffles)-t):
            self.riffles[i].bend_ratio2 = rs.CurveCurvature(self.Thalweg, self.riffles[i].parameter)[3]
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

        for i in range(len(self.points)-t):
            n = self.riffles[i].bend_ratio
            new_bend_ratio = (n - old_min) / old_range * new_range + new_min
            self.riffles[i].bend_ratio = new_bend_ratio
        return
    
    #getSlopes defines the *discrete* slopes of the line, based on the straight distance between points on the line
    def getSlopes(self, winChannel, winValley):
        
        #Channel Slope
        for i in range(len(self.riffles)):
            t1 = min([i, winChannel])
            t2 = min([len(self.riffles)-i-1, winChannel])
            sta1 = self.riffles[i - t1].station
            sta2 = self.riffles[i + t2].station
            pt1_z = self.riffles[i - t1].pt.Z
            pt2_z = self.riffles[i + t2].pt.Z
            self.riffles[i].channel_slope = (pt1_z - pt2_z)/(sta1 - sta2)
            print('STA:', self.riffles[i].station, '; Channel Slope:', self.riffles[i].channel_slope, '; winChannel:', winChannel, '; t1:', t1, ' t2:', t2, )         

        #Valley Slope
        for i in range(len(self.riffles)): 
            t1 = min([i, winValley])
            t2 = min([len(self.riffles)-i-1, winValley])
            print(len(self.riffles), i, t1, t2)
            sta1 = self.riffles[i - t1].station
            sta2 = self.riffles[i + t2].station
            pt1_z = self.riffles[i - t1].elevBankLow
            pt2_z = self.riffles[i + t2].elevBankLow
            self.riffles[i].valley_slope = (pt1_z - pt2_z)/(sta1 - sta2)
        return


class StreamPoint(object):
    """docstring for ClassName"""
    #Notes to think about:
    # -Does difference in left/right bank elevation matter in design?

    def __init__(self, point, crvCenterline, crvBankRight, crvBankLeft, station, lenDivision):
        #Define Initial Values
        self.pt = point
        self.parameter = rs.CurveClosestPoint(crvCenterline, point)     #Parameter (t) for point on centerline
        self.tangent = rs.CurveTangent(crvCenterline, self.parameter)
        self.slopeAtPoint = self.tangent[2]
        self.channel_slope = None
        self.valley_slope = None
        self.station = station
        self.bend_ratio = None
        self.bend_ratio2 = None
        self.index = int(self.station/lenDivision)
        self.suitability = 0
        self.use = None                    #1 = Riffle, 0 = Don't Use, -1 = Pool (pool points not usedd for now)

        #Bank Information
        self.ptBankRight = rs.EvaluateCurve(crvBankRight, rs.CurveClosestPoint(crvBankRight, self.pt))
        self.ptBankLeft = rs.EvaluateCurve(crvBankLeft, rs.CurveClosestPoint(crvBankLeft, self.pt))
        self.bank_width = horizontal_distance(self.ptBankRight, self.ptBankLeft)
        self.BankRightIncision = self.ptBankRight.Z - self.pt.Z 
        self.BankLeftIncision = self.ptBankLeft.Z - self.pt.Z 
        self.elevBankLow = min(self.ptBankLeft.Z, self.ptBankRight.Z)
        self.valley_slope = None

        #Proposed Riffle Design Information
        self.riffle = RifflePoint()
        self.pool = PoolPoint()
        self.geometry = None
        
        #project Thalweg to Horizontal Plane
        crvCenterlineHoriz = crvCenterline
        rs.ScaleObject(crvCenterlineHoriz, (0,0,0), (1,1,0))
        self.parameterHorizontal = rs.CurveClosestPoint(crvCenterlineHoriz, point)


class RifflePoint(object):
    
    def __init__(self):
        #Proposed Riffle Design Information
        self.length = None
        self.slope = None
        self.drop = None
        self.width = None     #Calc based on Bank Width
        self.depth = None
        self.station_start = None 
        self.station_end = None
    
class PoolPoint(object):

    def __init__(self):
        #Proposed Riffle Design Information
        self.length = None
        self.slope = None
        self.drop = None
        self.width = None     #Calc based on Bank Width
        self.station_start = None
        self.station_end = None
               


def horizontal_distance(pt1, pt2):
    distance = math.sqrt(math.pow(pt2.X - pt1.X, 2) + math.pow(pt2.Y - pt1.Y, 2)) 
    return distance

#x is set as curve in centerline class
crvRifflePoints = Centerline(crvThalweg, crvRightBank, crvLeftBank, interval)

    

# attr = []
# attr.append('pt.Z')
# attr.append('parameter')
# attr.append('tangent')
# attr.append('slopeAtPoint')
# attr.append('channel_slope')
# attr.append('valley_slope')
# attr.append('station')
# attr.append('bend_ratio')
# attr.append('ptBankRight')
# attr.append('ptBankLeft')
# attr.append('bank_width')
# attr.append('BankRightIncision')
# attr.append('BankLeftIncision')
# attr.append('elevBankLow')
# attr.append('valley_slope')
# attr.append('riffle_length')
# attr.append('riffle_slope')
# attr.append('riffle_drop')
# attr.append('riffle_width')
# attr.append('geometry')

def getIdealRiffleDesign(self, riffle_drop_min, riffle_length_min): 
	#2017.11.27
        ##need an additional variable - that is able to be reset

        #Calculate Ideal riffle design for each stream point
        for i in self.riffles:
            check = False
            count = 0
            riffle_drop_test = riffle_drop_min
            riffle_length_test = riffle_length_min
            
            #loop through sizing scenarios
            while check == False and count < 35:
                
                print('channel slope;', i.channel_slope)
                if i.channel_slope == 0: 
                    pool_length = 10000
                else:  
                    pool_length = abs((riffle_drop_test / i.channel_slope) - riffle_length_test)

                print('STA=', i.station, '; Valley Slope=', i.channel_slope, '; PL=', pool_length, '; rLt=', riffle_length_test, '; rDt=', riffle_drop_test)
                if pool_length >= riffle_length_test:
                    i.geometry = "Riffle"
                    i.riffle.length = riffle_length_test
                    i.riffle.drop = riffle_drop_test
                    i.riffle.slope = riffle_drop_test / riffle_length_test
                    i.riffle.station_end = i.station + i.riffle.length
                    
                    #!!!This need to be adjusted, was only in because bad LiDAR
                    if pool_length == 10000:
                        i.pool.length = i.riffle.length
                    else:
                        i.pool.length = pool_length
                    i.pool.station_start = i.riffle.station_end
                    i.pool.station_end = i.station + i.riffle.length + i.pool.length
                    check = True
                else:
                    if riffle_length_test < 30:
                        riffle_length_test += 5
                        count +=1
                    elif riffle_drop_test < 2:
                        riffle_length_test = riffle_length_min
                        riffle_drop_test += 0.25
                        count +=1
                    else:
                        i.geometry = "Neither"
                        check = True
        return