#!/usr/bin/env python

### Script to define scan grid

### Authors:
### Manuel Franco Sevilla
### Ana Ovcharova

import os,sys,math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grid_utils import *

model = "T6ttHZ_BR-H_0p6"
process = "StopStop"

period = "Fall17"
#period = "Summer16"

# Number of events for mass point, in thousands
if "16" in period : nevt = 400
elif "17" in period : nevt = 450

diag_low, diag_high = 100, 10
xmin, xmax, xstep = 300, 1000, 50
ymin, ymax, ystep_low, ystep_high = 175, 1000, 50, 25


# -------------------------------
#    Constructing grid

mpoints_tmp = []
for mx in range(xmin, xmax+1, xstep):
  ylist = []
  if mx > (ymax + (diag_low - diag_high)):
    ylist.extend(range(ymin, ymax+1, ystep_low))
    ylist.append(ymax)
  elif mx > ymax:
    ylist.extend(range(ymin, mx - diag_low, ystep_low))
    ylist.extend(range(mx - diag_low, ymax+1, ystep_high))
  else:
    ylist.extend(range(ymin, mx - diag_low, ystep_low))
    ylist.extend(range(mx - diag_low, mx-diag_high+1, ystep_high))
  for my in ylist:
    mpoints_tmp.append([mx,my,nevt])


mpoints = []
for i,point in enumerate(mpoints_tmp): 
  mx, my, nevt = point[0], point[1], point[2]
  if mx - my == 125.: my = int(mx -126.)
  mpoints.append([mx,my,nevt])

# for i,point in enumerate(mpoints): print i,point
    
## Test print out for repeated points
mset = set()
for mp in mpoints: mset.add(mp[0]*10000+mp[1])
Npts, Ndiff = len(mpoints), len(mset)
if Npts==Ndiff: print "\nGrid contains "+str(Npts)+" mass points. No duplicates\n"
else: print "\n\nGRID CONTAINS "+str(Npts-Ndiff)+" DUPLICATE POINTS!!\n\n"

# -------------------------------
#     Plotting and printing

Ntot = makePlot([mpoints], 'events', model, process, xmin, xmax, ymin, ymax)

print '\nScan contains '+"{0:.0f}".format(Ntot*1000)+" events"
print 'Average matching efficiency (for McM and GEN fragment) = '+"{0:.3f}".format(getAveEff(mpoints,process))

print
