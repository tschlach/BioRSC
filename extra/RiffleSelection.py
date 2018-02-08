import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 
import time
from operator import itemgetter
from copy import deepcopy 

#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy



def place_Riffles(centerline):
 
    #???? Do I need to have copy or point to original? 


    iMax = None                     #index of riffle with max value, which equals index of list of Riffles
    iSet = None                     #index of riffle to set "use" = 1
    max_Suitability = None
    gapTolerance = 20               #Feet between riffle structures that could still have a structure
    suitTol = 0.90                  #Tolerance for selecting to move riffle
 

    #Remove riffles at end that do not have length in centerline for pool
    remove_endRiffles(centerline)

    #Loop Through values (while?)
    #Get Max Value (just bend for now, later to be a weighted value)
    for i in range(len(centerline.riffles)):
        #need to use range(len)) in order check all riffles, not necessarily in order though
        #??Can I set a riffle to a specific one in teh centerline? to shorten code. Will it
        #??change the original? (i.e. riffleMax = centerline.riffles[iMax])
        print('')
        print('-----Place Riffle----i=', i)

        #STEP 1: FIND MAX RIFFLE SUITABILITY VALUE
        #
        #---------------------
        iMax, max_Suitability = maxSuitability(centerline)
            #All riffles[].use != None are filtered out in maxSuitability

        #Check that max_Suitability is acceptable value
        if max_Suitability == None or max_Suitability <= 0:
            continue
                
        #iSet = iMax #???GEt rid of now?
        
        rMax = centerline.riffles[iMax] 
        #rCopy = deepcopy(centerline.riffles[iMax])
            #deepcopy make new instance, not just pointer. using this for now so that changes are 
            #made until final


        #COMMENTS:
            #1. Find Max of Suitability Rating
            #2. iMax: Index of riffle (centerline.riffles[] with the max value 


        #STEP 2:
        #TEST FITNESS
        #---------------------
        
        #2a. Find upstream (US) gaps
        iUS, gapUS = find_gapUS(centerline, iMax)

        #2b. CHECK UPSTREAM TO SEE IF BETTER POINT RELATIVE TO US RIFFLE
        #THIS MAY LEAVE GAP
        if iUS!= None and gapUS < gapTolerance:
            
            rUS = centerline.riffles[iUS]
            
            #Is there a better solution upstream?
            #for i in range(iUS, iMax, 1):
            for j in centerline.riffles[iUS:iMax]: 
                if j.suitability > rMax.suitability * suitTol:
                    rMax = j
                    iMax = rMax.index
                    print(iUS, j, 'should stop here')
                    break 
                    
            #     print(iUS, j.index, 'broke if statement', 'current Suitability:', j.suitability, 'target Suit:', rMax.suitability*suitTol)
            # print(iUS, i.index, 'broke for statement', 'current Suitability:', i.suitability, 'target Suit:', rMax.suitability*suitTol)

                    #No need to check upstream now that best US was selected through start of loop
                     
        
        #2c.
        #Get closest "placed" downstream riffle
        iDS, gapDS = find_gapDS(centerline, iMax)
            #?????Should find_gapDS stop at end of riffle/pool length? That's all it is currently used for

        #Check if riifle/pool overlaps next DS riffle 
        if iDS != None:
            rDS = centerline.riffles[iDS]
                        
            print(rMax.pool.station_start, rMax.pool.length, rMax.pool.station_end)
            
            #if the next downstrean riffle is within the current riffle/pool length then go to next i
            #XXif iDS_STA < iMax_STA_poolEnd:
            if rDS.station < rMax.pool.station_end:  
                
                #OLD DECISION TREE - NEED TO UPDATE 
                #CHECK NEXT US STREAM POINT IS WITHIN SUIT TOLERANCE (ORGINAL)
                    #YES - MOVE TO NEXT US STREAM POINT, START OVER 
                    #NO - CHECK IF NEXT DS RIFFLE POINT IS WITHIN POOL MIN
                        #YES - SET RIFFLE/POOL AS 0
                        #NO - SET RIFFLE AS 1, POOL LENGTH = NEXT DS RIFFLE POINT AND 0s



                print('Next DS riffle within length of riffle/pool. Removed from consideration')
                
                #Set .use = 0
                # print('iDS=', iDS, '; iMax =', iMax)
                for i in range(iMax, iDS, 1):
                    #Make "use" = 2 for Gaps
                    centerline.riffles[i].use = 2
                continue    #breaks out of "if" loop??
            
            else:
                print('No DS riffle within length of riffle/pool')

                #CHECK IF pool.station_end - riffle[next ds].station < lenDivision
                    #YES - SET RIFFLE AS 1, POOL AS 0
                    #NO - IS NEXT DS STREAM POINT WITHIN SUIT TOLERANCE (ORIGINAL)
                        #NO - SET ORIGINAL RIFFLE = 1, POOLS = 0
                        #YES - MOVE TO NEXT DS STREAM POINT, START OVER

        else:
            print('No DS riffle')




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
        print('Riffled placed at=', rMax.station)
        print('riffle start: ', rMax.station,'Riffle end: ', rMax.riffle.station_end, 'Pool end: ', rMax.pool.station_end,'Pool Length: ', rMax.pool.length)

        
        #Use riffle at rMax, Set all other values within rMax riffle/pool as 0
        rMax.use = 1
        print(rMax.index, rMax.pool.station_end, int(rMax.pool.station_end/centerline.lenDivision) )
        for i in range(rMax.index + 1, int(rMax.pool.station_end/centerline.lenDivision), 1):
            centerline.riffles[i].use = 0
        

        #????Need to go back to this
        # #Set Non-Riffles to 0
        # iSetUS = centerline.riffles[iSet].station
        # iSetDS = centerline.riffles[iSet].pool.station_end
        # for i in centerline.riffles:
        #     if iSetUS < i.station < iSetDS:
        #         if i.use == None:
        #             i.use = 0

        #COMMENTS:
            #1. Should we ever cut upstream pool short?

        # print(centerline.riffles[iSet].use)



        #STEP 4
        #ADJUST RIFFLES TO PREVENT GAPS AS NEEDED
        #---------------------

        #COMMENTS:





        #REPEAT STEPS 1 THROUGH 4 UNTIL DONE


    return 

def resolve_Gaps(centerline):

    print('-----RESOLVE GAPS----', )
    print (len(centerline.riffles))

    for i in range(len(centerline.riffles)-1, 0, -1):
        
        print(centerline.riffles[i].index, centerline.riffles[i].use)

        if centerline.riffles[i].use == 2:
            
            print('set pEnd =', i + 1)
            pEnd = centerline.riffles[i + 1]

            for j in range(i, 0, -1):

                if centerline.riffles[j].use == 1:
                    print('set r =', j) 

                    r = centerline.riffles[j]
                    r.riffle.pt_end = rs.coerce3dpoint((r.riffle.pt_end.X, r.riffle.pt_end.Y, pEnd.riffle.pt_start.Z))
                    r.pool.pt_start = r.riffle.pt_end
                    r.pool.pt_end = pEnd.riffle.pt_start
                    r.pool.station_end = pEnd.riffle.station_start
                    r.pool.tangent_end = pEnd.tangent

                    for k in range (i, j, -1):
                        if centerline.riffles[k].use == 2:
                            centerline.riffles[k].use = 0

                    #?? Need to rewrite gaps .use values
                    break

    return 

def remove_endRiffles(cl):

    for i in cl.riffles:
        if i.pool.station_end > cl.riffles[len(cl.riffles)-1].station:
            i.use = 0
            print(i.station)
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
        #??Should be able to rewrite as for i in cl.riffles[X:]
        if cl.riffles[i].use == 0:
            iUS = i + 1
            print(i-1, cl.riffles[i-1].index, cl.riffles[i-1].use, i, cl.riffles[i].index, cl.riffles[i].use, i+1, cl.riffles[i+1].index, cl.riffles[i+1].use)
            print('iUS=', i + 1, ';icurrent=', iCurrent, ';iUS STA_start=', cl.riffles[i + 1].pool.station_end,  'iMax STA_end=', cl.riffles[iCurrent].station)
            
            #pool.station_end may be none, so set to .station_end
            #one of these is returning neg values for gapUS
            if cl.riffles[i + 1].pool.station_end == None:
                gapUS = cl.riffles[iCurrent].station - cl.end
                print('1: iUS= ', iUS, ' ;gapUS= ', gapUS)
                return iUS, gapUS
            else:    
                gapUS = cl.riffles[iCurrent].station - cl.riffles[i + 1].pool.station_end
                print('2: iUS= ', iUS, ' ;gapUS= ', gapUS)
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
            #??This will eventually mean that the "place_riffles" loop does not go through all riffles, does this matter?

            #print('iUSE')
            if i.suitability > max_suitability:
                #print('T3')
                max_suitability = i.suitability
                iMax = i.index                      #???This could probably ust be =i
    print('maxSuit=', max_suitability, 'iMax=', iMax, 'i', i)
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


time_start = time.time()
print(time_start)
#___________________________________________________________________________
#STEP 0: RESET USES
#___________________________________________________________________________
print('STEP 0---------------')
for i in crvRifflePoints.riffles:
   i.use = None

print('# of Stream Points =', len(crvRifflePoints.riffles))

for i in crvRifflePoints.riffles:
    print(i.suitability)
    

time_step0 = time.time()
print(time_step0-time_start)

#___________________________________________________________________________
#STEP 1:  PLACE RIFFLES
#Place Riffles
#___________________________________________________________________________
print('STEP 1---------------')
place_Riffles(crvRifflePoints)


time_step1 = time.time()
print(time_step1-time_start)

#___________________________________________________________________________
#STEP 2:  Resolve Gaps
#Place Riffles
#___________________________________________________________________________
print('STEP 2---------------')
resolve_Gaps(crvRifflePoints)



time_step2 = time.time()
print(time_step2-time_start)

print('DONE---------------')
for i in crvRifflePoints.riffles:
    print('i=', i.index, '; Use =', i.use)


time_step3 = time.time()
print(time_step3-time_start)

