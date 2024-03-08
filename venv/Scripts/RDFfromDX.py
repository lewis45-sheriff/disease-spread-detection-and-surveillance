#!C:\Users\lewis kipkemoi\Desktop\diseasesurveillance\venv\Scripts\python.exe
import grid.grid as grid
import sys
print "# Input format: RDFfromDX.py <dxfilename> <x> <y> <z> <delta> <max> (concentration)"
print "If you input a concentration (particles per unit volume), the coordination number will also be printed in the 3rd column"

if len(sys.argv) < 6:
    quit("Error, insufficient arguments")

dxfilename, x, y, z, delta, maxval = sys.argv[1:7]

concentration = False
if len(sys.argv) > 7:
    concentration = float(sys.argv[7])

griddata = grid.dx2Grid(dxfilename)
if not concentration:
    rdf = griddata.interpRDF([float(x),float(y),float(z)], float(delta), float(maxval))
    for i, value in enumerate(rdf):
        print i*float(delta), value
else:
    rdf, coordnums = griddata.interpRDF([float(x),float(y),float(z)], float(delta), float(maxval), concentration)
    for i, value in enumerate(rdf):
        print i*float(delta), value, coordnums[i] 
