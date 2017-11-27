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
    max_Suitability = None
    gapTolerance = 20               #Feet between riffle structures that could still have a structure
    suitTol = 0.90                  #Tolerance for selecting to move riffle
 
    #Loop Through values (while?)
    #Get Max Value (just bend for now, later to be a weighted value)
    for i in range(0,50,1):
        print('')
        print('-----Place Riffle----i=', i)

        #STEP 1: FIND MAX RIFFLE SUITABILITY VALUE
        #
        #---------------------
        iMax, max_Suitability = maxSuitability(centerline)

        if max_Suitability == None or max_Suitability <= 0:
                continue
                
        iSet = iMax
        #COMMENTS:
            #1. Find Max of Suitability Rating
            #2. iMax: Index of riffle (centerline.riffles[] with the max value 


        #STEP 2:
        #TEST FITNESS
        #---------------------
        
        #Get closest "placed" downstream riffle
        iDS, gapDS = find_gapDS(centerline, iMax)
        
        #2a. Check if riifle/pool overlaps next DS riffle 
        if iDS != None:
            #Get Station of iDS, only if it returns a non-"None" value
            iDS_STA = centerline.riffles[iDS].station
            iMax_STA_poolEnd = centerline.riffles[iMax].pool.station_end

            #if the next downstrean riffle is within the current riffle/pool length then go to next i
            if iDS_STA < iMax_STA_poolEnd:
                print('Next DS riffle within length of riffle/pool. Removed from consideration')
                
                #Set .use = 0
                # print('iDS=', iDS, '; iMax =', iMax)
                for i in range(iMax, iDS, 1):
                    centerline.riffles[i].use = 0
                continue
            else:
                print('No DS riffle within length of riffle/pool')
        else:
            print('No DS riffle')


        #2b. Find upstream (US) gaps
        iUS, gapUS = find_gapUS(centerline, iMax) 
            #Comment: Returns "None" for all values not found

        # print("iUS=", iUS, "gapUS=", gapUS,"iDS=", iDS,"gapDS=", gapDS)

        #2c. CHECK UPSTREAM TO SEE IF BETTER POINT
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
        print('iSet=', iSet)
        centerline.riffles[iSet].use = 1
        print('riffle start: ', centerline.riffles[iSet].station,'Riffle end: ', centerline.riffles[iSet].pool.station_end)

        #Set Non-Riffles to 0
        iSetUS = centerline.riffles[iSet].station
        iSetDS = centerline.riffles[iSet].pool.station_end
        for i in centerline.riffles:
            if iSetUS < i.station < iSetDS:
                if i.use == None:
                    i.use = 0

        #COMMENTS:
            #1. Should we ever cut upstream pool short?

        # print(centerline.riffles[iSet].use)



        #STEP 4
        #ADJUST RIFFLES TO PREVENT GAPS AS NEEDED
        #---------------------

        #COMMENTS:





        #REPEAT STEPS 1 THROUGH 4 UNTIL DONE


    return 

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

def find_gapUS(cl, iCurrent):
    #cl:  centerline class
    #iCurrent: index of current riffle  

    print('find_GapsUS, iCurrent=', iCurrent)

    for i in range(iCurrent-1, 0, -1):
        # print('fg i=', i)
        if cl.riffles[i].use == 0:
            iUS = i
            print('i=', i, ';icurrent=', iCurrent, ';STA_start=', cl.riffles[i].pool.station_end,  ';STA_end=', cl.riffles[iCurrent].station)
            
            #pool.station_end may be none, so set to .station_end
            if cl.riffles[i].pool.station_end == None:
                gapUS = cl.riffles[iCurrent].station - cl.end
                print('iUS= ', iUS, ' ;gapUS= ', gapUS)
                return iUS, gapUS
            else:    
                gapUS = cl.riffles[iCurrent].station - cl.riffles[i].pool.station_end
                print('iUS= ', iUS, ' ;gapUS= ', gapUS)
                return iUS, gapUS

    return None, None


def find_gapDS(cl, iCurrent):
    #cl:  centerline class
    #iCurrent: index of current riffle  
    
    print('find_GapsDS, iCurrent=', iCurrent)
    
    for i in range(iCurrent + 1, len(cl.riffles), 1):
        if cl.riffles[i].use == 1:
            iDS = i
            gapDS = cl.riffles[i].station - cl.riffles[iCurrent].pool.station_end
            print('iDS= ', iDS, ' ;gapDS= ', gapDS)
            return iDS, gapDS

    return None, None

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
    print('max=', max_suitability, 'iMax=', iMax, 'i', i)
    return iMax, max_suitability

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
print('STEP 0---------------')
for i in crvRifflePoints.riffles:
   i.use = None

print('# of Stream Points =', len(crvRifflePoints.riffles))

for i in crvRifflePoints.riffles:
    print(i.suitability)
    
#___________________________________________________________________________
#STEP 1: CALCULATE STREAM POINT SUITABILITIES
#Adjust the riffles.suitability values for each stream points
#___________________________________________________________________________
print('STEP 1---------------')
calculate_Suitability(crvRifflePoints)
#Print Suitability Here*********************************

#___________________________________________________________________________
#STEP 2: PLACE RIFFLES
#Place Riffles
#___________________________________________________________________________
print('STEP 2---------------')
place_Riffles(crvRifflePoints)



print('DONE---------------')
for i in crvRifflePoints.riffles:
    print('i=', i.index, '; Use =', i.use)


