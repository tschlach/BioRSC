import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 
from operator import itemgetter 

#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy


TierR1 = []
TierR2 = []
TierR3 = []
TierP1 = []
TierNull = []

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
   
    return  list_values




def calculate_Suitability(centerline):

    #Filter 1
    for i in centerline.riffles:
        if i.geometry == "Riffle":                   #Geometry Check
            i.suitability = i.bend_ratio2

        elif i.geometry == "Pool":                   #Geometry Check
            i.suitability = -i.bend_ratio2

        else:
            i.suitability = 0
    return 

# def get_RiffleTiers(list_values):

#     #Filter 1
#     for i in range(len(list_values)):
#         if list_values[i][12] == "Riffle":                   #Geometry Check
#             if list_values[i][2] > 10:                       #Bend_ratio Check (value random, need to select)
#                 TierR1.append(list_values[i])
#             elif list_values[i][2] > 5:
#                 TierR2.append(list_values[i])
#             else:
#                 TierR3.append(list_values[i])
#         elif list_values[i][12] == "Pool":                   #Geometry Check
#             TierP1.append(list_values[i])
#         else:
#             TierNull.append(list_values[i])
#     return 

def place_Riffles(centerline):
    

    iMax = None                      #index of listMain (LM) for current riffle with max value, which equals index of list of Riffles
    gapTolerance = 20               #Feet for opening


    iLM_Next = None                     #index of listMain (LM) for next riffle, which equals index of list of Riffles 
    list_Final = []
    removeLowerLimit = None
    removeUpperLimit = None
    iTier = None                        #index of value relative to current Tier
    iTier_Max = None

    # list_Final.append(listAll[0])        

    #+++++++++++
    #search 1
    #+++++++++++
    # test = 0

    #Loop Through values (while?)
    #Get Max Value (just bend for now, later to be a weighted value)
    for i in range(5): # and test < 5:
        
        #STEP 1:
        #FIND MAX VALUE
        #---------------------
        iMax = maxSuitability(centerline)
        #COMMENTS:
            #1. Find Max of Suitability Rating
            #2. iMax: Index of riffle (centerline.riffles[] with the max value 


        #STEP 2:
        #TEST FITNESS
        #---------------------
        iUS, gapUS, iDS, gapDS = find_Gaps(centerline, iMax)


        #CHECK UPSTREAM TO SEE IF BETTER POINT
        #THIS MAY LEAVE GAP
        if iUS!= None and gapUS < gapTolerance:
            #Is there a better solution upstream?


        #CHECK DOWNSTREAM IF THE RIFFLE/POOL WILL FIT
        #AND IF IT NEEDS TO LENGTHEN IT BECAUSE DISTANCE < 20 FEET
        #     check_Fitness(centerline, iUS, iMax) if iUS != None   
        

        #     check_Fitness(centerline, iUS, iMax) if iDS !=None      



            #-Check station of selected riffle relative to upstream and downstream riffle already placed
            #-If within a certain distance, adjust upstream and downstream riffle and remove others from list




        #COMMENTS:
            #1. CHECK US AND DS TO SEE IF RIFFLE VALUE IS WITHIN A TOLERANCE (SAY 5% OF CURRENT VALUE)
            #   > THIS MAY LEAD TO A BETTER FIT VALUE RELATVIE TO AN UPSTREAM OR DOWNSTREAM RIFFLE 



        #STEP 3:
        #PLACE RIFFLE IN FINAL LIST
        #---------------------

        #COMMENTS:




        #STEP 4
        #ADJUST RIFFLES TO PREVENT GAPS AS NEEDED
        #---------------------

        #COMMENTS:




        #STEP 5
        #DELETE MINIMUM AMOUNT OF RIFFLES
        #---------------------

        #COMMENTS:


        #STEP 6 
        #SORT RIFFLES
        #---------------------

        #COMMENTS:




        #REPEAT STEPS 1 THROUGH 3 UNTIL DONE

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

    return #list_Final


def check_Fitness(cl, iUS, iDS, tol):

    for i in range(iUS, iDS, 1)

        #Compare Suitability
        if cl.riffles[i].suitability > (1-tol) * cl.riffles[iDS].suitability:
            #Move selected riffle to new furthest upstream riffle within tolerance
            return i


    return 


def find_Gaps(cl, iCurrent):
    #cl:  centerline class
    #iCurrent: index of current riffle  
    iUS = None              #index of Upstream riffle already flagged
    iDS = None              #index of Downstream riffle already flagged
    gapUS = None
    gapDS = None

    #FIND UPSTREAM RIFFLE
    for i in range(iCurrent-1, 0, -1):
        if cl.rifles[i].use == 0:
            iUS = i
            gapUS = cl.riffles[iCurrent].station - cl.riffles[i].pool.station_end  

    #FIND DOWNSTREAM RIFFLE
    for i in range(iCurrent + 1, len(cl.riffles), 1):
        if cl.rifles[i].use == 1:
            iDS = i
            gapDS = cl.riffles[i].station - cl.riffles[iCurrent].pool.station_end

    return iUS, gapUS, iDS, gapDS

def maxSuitability(cl):
    #l =  list of variables
    #v = index of variable looking for 
    max_val = None
    num = None

    for i in cl.riffles:
        if i.riffles.use != 0 or i.riffles.use != -1:
            if i.riffles.suitability > max_suitability:
                max_suitability = i.riffles.suitability
                iMax = i.riffles.index                      #???This could probably ust be =i
    print(max_suitability, iMax, i)
    return iMax

def nearestList(l, v, value):
    #l =  list of variables
    #v = variable looking for
    #value = value looking for nearest to 
    min_d = 100000000000
    near_val = None
    num = None

    for i in range(len(l)):
        d = abs(l[i][v]-value)
        if d < min_d:
            near_val = l[i][v]
            near_idx = l[i][0]
            min_d = d
            num = i

    return near_idx, near_val, numi

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
    return None, None

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
    return

def print_RiffleInfo(l, i):
    print("----------")
    print("index = ", i)
    print("Station = ", l.station)
    print("Invert Elev = ", l.pt.Z)
    print("Riffle Drop = ", l.riffle.drop)
    print("Riffle Length = ", l.riffle.length)
    print("Radius of Curvature = ", l.bend_ratio2)
    return

def sort_list(l):



    return l


calculate_Suitability(crvRifflePoints)

for i in crvRifflePoints.riffles:
    print(i.suitability)


# listMaster = get_VariableArray(crvRifflePoints)

# get_RiffleTiers(listMaster)

# listFinal = place_Riffles(crvRifflePoints, listMaster)

# listFinalSorted = sorted(listFinal, key=itemgetter(1))

# Riffles = []

# for i in listFinalSorted:
#     Riffles.append(crvRifflePoints.riffles[i[0]])




# print("TierR1")
# print(TierR1)
# print("TierR2")
# print(TierR2)
# print("TierR3")
# print(TierR3)
# print("TierP1")
# print(TierP1)
# print("TierNull")
# print(TierNull)  

#Riffles = suitability(crvRifflePoints)
# print(Riffles)