"""
Author: Biohabitats Inc.
Updated: October 26, 2017

This script takes a centerline curve and returns the idealized riffle start locations, as determined by the 'suitability analysis'

Dependencies:
    -BioRSC Window class

Tasks:
    -the suitability file should take a centerline class and return idealized points for placing riffles (or points - or riffle/points)
    -weighting mechanism
    -testing windows of different length for suitability
    -
"""

######

def create_window_dict(curve):
    windows = {}

    counts = ["%03d" % x for x in range(len(curve.points))] 

    count = 0
    for i in curve.points:
        window = Window(curve.curve, i, curve.points, 40) ###would be nice to test this for different lengths...
        window.span_test()
        window.generate(window.span_test())
        window.getParameters()
        windows["Window" + counts[count]] = {
        "index": counts[count],
        "position_on_line": int(counts[count])/2,
        "slope": window.slope,
        "drop": window.drop,
        "p_ratio": window.p_ratio,
        "length": window.length,
        "start_height": window.start_height,
        "end_height": window.end_height
        }
        count += 1  

    return windows

#takes a list window dictionaries.
def suitability(windows):
    windows2 = []
    windows3 = []

    #p-ratio
    for key,value in windows.items():
        if value[4] < 1:
            windows2.append(key)
    #drop
    for key, value in windows.items():
        if key in windows2:
            if value[3] < -0.25:
                windows3.append(key)

    return windows3

##windows 3 is simply a list of windows that meet the criteria outlined in the above 'if' loops