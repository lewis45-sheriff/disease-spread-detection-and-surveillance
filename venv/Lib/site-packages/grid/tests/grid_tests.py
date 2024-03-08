#!/usr/bin/env python
import grid.grid as grid
import numpy as np
import os

datadir = os.path.join(os.path.dirname(grid.__file__),"tests","data")


print "Testing reading TINKER guv files.."
datafilename = os.path.join(datadir,'TKRguv','h2o.guv.sample')
dists = grid.TKRguv2Grids(datafilename)
assert len(dists) == 2
assert 1.1 > dists[0].distribution[31,31,31] > 0.9


print "Testing reading UxDATA files.."
uxdatafilename = os.path.join(datadir,'UxDATAfiles','UVDATA.sample')
uxdists = grid.data2Grids(uxdatafilename, disttypes=['g','c'])
assert len(uxdists) == 4
assert 1.1 > uxdists['O.g'].distribution[31,31,31] > 0.9

dxfilename = os.path.join(datadir, "dxfiles", 
                          "AlaDP_3DRISM_smallbuffer.dx.gz") 
griddata = grid.dx2Grid(dxfilename)

print "Testing Trilinear interpolation.."
assert griddata.getvalue([9.0,1.0,1.0]) - 0.609013742553 <  1 * 10**(-10)

# Test 3D->RDF function.
print "Testing RDF interpolation..."
rdfnearO = griddata.interpRDF([3.6, 6.653, 0.00], 0.1, 10.0) #Carbonyl O
rdfnearH = griddata.interpRDF([6.737, 6.359, 0], 0.1, 10.0) #NH H
rdfnearH2 = griddata.interpRDF([2.733, 4.556, 0], 0.1, 10.0) #another NH H
#Debugging section 

#import matplotlib
#import pylab
#from numpy import arange
#xset = arange(0, 10.0, 0.1)
#matplotlib.pyplot.scatter(xset, rdfnearH, color="silver")
#matplotlib.pyplot.scatter(xset, rdfnearO, color="red")
#matplotlib.pyplot.scatter(xset, rdfnearH2, color="blue")
#matplotlib.pyplot.show()
#quit()

# Test reading/writing
print "Testing reading/writing dx files.."
originalgrid = grid.dx2Grid(dxfilename)

maxvalue = originalgrid.distribution.max()
maxindices = tuple(np.argwhere(originalgrid.distribution == maxvalue)[0])
originalgrid.distribution[maxindices] = maxvalue * 2.0
originalgrid.writedx("modified.dx")
newgrid = grid.dx2Grid("modified.dx")
newmax = newgrid.distribution.max()
assert newmax == maxvalue * 2.0
#cleanup
del originalgrid
del newgrid
os.remove("modified.dx")

# Test shells
print "Testing shell-related utilities.."
storedprecomputedshells = grid.readshellindices()
newshells = grid.precomputeshellindices(40)
for storedshell, newshell in zip(storedprecomputedshells, newshells):
    for storedpoint, newpoint in zip(storedshell, newshell):
        for storedindex, newindex in zip(storedpoint, newpoint):
            assert storedindex == newindex

