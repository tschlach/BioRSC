import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 
from operator import itemgetter 

#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy






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

def place_Riffles(centerline):
 
    iMax = None                     #index of riffle with max value, which equals index of list of Riffles
    iSet = None                     #index of riffle to set "use" = 1
    gapTolerance = 20               #Feet between riffle structures that could still have a structure
    suitTol = 0.90                  #Tolerance for selecting to move riffle
 
    #Loop Through values (while?)
    #Get Max Value (just bend for now, later to be a weighted value)
    for i in range(0,10,1):
        
        #STEP 1: FIND MAX RIFFLE SUITABILITY VALUE
        #
        #---------------------
        iMax = maxSuitability(centerline)
        iSet = iMax
        #COMMENTS:
            #1. Find Max of Suitability Rating
            #2. iMax: Index of riffle (centerline.riffles[] with the max value 


        #STEP 2:
        #TEST FITNESS
        #---------------------
        #2a. Find gaps if iMax placed
        iUS, gapUS, iDS, gapDS = find_Gaps(centerline, iMax)
            #Returns None for all values not found

        print("iUS=", iUS, "gapUS=", gapUS,"iDS=", iDS,"gapDS=", gapDS)

        #2b. CHECK UPSTREAM TO SEE IF BETTER POINT
        #THIS MAY LEAVE GAP
        if iUS!= None and gapUS < gapTolerance:
            #Is there a better solution upstream?
            for i in range(iUS, iMax, 1):
                if centerline.riffles[i].suitability > (centerline.riffles[iMax].suitability) * suitTol:
                    iSet = i


        #2.c CHECK DOWNSTREAM IF THE RIFFLE/POOL WILL FIT
        #AND IF IT NEEDS TO LENGTHEN IT BECAUSE DISTANCE < 20 FEET
        #     check_Fitness(centerline, iUS, iMax) if iUS != None   
        ###################################################
        ######################SKIPPED######################
        ###################################################

        #     check_Fitness(centerline, iUS, iMax) if iDS !=None      



            #-Check station of selected riffle relative to upstream and downstream riffle already placed
            #-If within a certain distance, adjust upstream and downstream riffle and remove others from list




        #COMMENTS:
            #1. CHECK US AND DS TO SEE IF RIFFLE VALUE IS WITHIN A TOLERANCE (SAY 5% OF CURRENT VALUE)
            #   > THIS MAY LEAD TO A BETTER FIT VALUE RELATVIE TO AN UPSTREAM OR DOWNSTREAM RIFFLE 



        #STEP 3: SET ISET AS RIFFLE
        #---------------------
        print(iSet)
        centerline.riffles[iSet].use = 1
        print('start: ', centerline.riffles[iSet].station)
        print('end= ', centerline.riffles[iSet].pool.station_end)

        #Set Non-Riffles to 0
        iSetUS = centerline.riffles[iSet].station
        iSetDS = centerline.riffles[iSet].pool.station_end
        for i in centerline.riffles:
            if iSetUS < i.station < iSetDS:
                i.use = 0

        #COMMENTS:
            #1. Should we ever cut upstream pool short?

        # print(centerline.riffles[iSet].use)



        #STEP 4
        #ADJUST RIFFLES TO PREVENT GAPS AS NEEDED
        #---------------------

        #COMMENTS:





        #REPEAT STEPS 1 THROUGH 4 UNTIL DONE

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

def set_RiffleUse(cl, iSet):
    #iSet: 


    return

def check_Fitness(cl, iUS, iDS, tol):

    for i in range(iUS, iDS, 1):

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

def maxSuitability(cl):
    #l =  list of variables
    #v = index of variable looking for 
    iMax = None
    max_val = None
    num = None
    max_suitability = None

    for i in cl.riffles:
        #print('Use:', i.use)
        if i.use == None:
            #print('iUSE')
            if i.suitability > max_suitability:
                #print('T3')
                max_suitability = i.suitability
                iMax = i.index                      #???This could probably ust be =i
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



def print_RiffleInfo(l, i):
    print("----------")
    print("index = ", i)
    print("Station = ", l.station)
    print("Invert Elev = ", l.pt.Z)
    print("Riffle Drop = ", l.riffle.drop)
    print("Riffle Length = ", l.riffle.length)
    print("Radius of Curvature = ", l.bend_ratio2)
    return



#___________________________________________________________________________
#STEP 0: RESET USES
#___________________________________________________________________________
for i in crvRifflePoints.riffles:
    i.use = None


#___________________________________________________________________________
#STEP 1: CALCULATE STREAM POINT SUITABILITIES
#Adjust the riffles.suitability values for each stream points
#___________________________________________________________________________
calculate_Suitability(crvRifflePoints)
#Print Suitability Here*********************************

#___________________________________________________________________________
#STEP 2: PLACE RIFFLES
#Place Riffles
#___________________________________________________________________________
place_Riffles(crvRifflePoints)


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