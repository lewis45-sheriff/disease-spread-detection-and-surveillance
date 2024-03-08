#!C:\Users\lewis kipkemoi\Desktop\diseasesurveillance\venv\Scripts\python.exe

'''Created by Daniel Sindhikara, sindhikara@gmail.com
Program converts various volumetric data formats.

For now only inputs UxDATA and TINKER guv files.
For now only outputs .dx files.
'''  

from __future__ import division

import grid.grid as grid
import sys
import argparse
import os

def main():
    parser = \
        argparse.ArgumentParser(description=''+
                    'Converts volumetric data via grid.py.\n'+
                    'Currently available formats:\n\n'+
                    "Input:\n"+
                    'OpenDX (.dx)\n'+
                    '3D-RISM TINKER "xuv" style (.guv, .huv, etc)\n'+
                    '3D-RISM GAMESS "UxDATA" style (UVDATA, VVDATA, etc)\n'+
                    'MDF 3D-RISM HDF5 "H5" style\n\n'+
                    'Output:\n'+
                    'OpenDX (.dx)\n'+
                    'Accelrys DS grid file (.grd) NOT UHBD grid!!!\n'+
                    'Input filetypes are determined by file names.')
    outtypes = ['dx', 'grd']
    parser.add_argument('inputfile', type=str, help='Input volumetric data file')
    parser.add_argument('outtype', type=str, help='Type of output file: %s' % outtypes)
    args = parser.parse_args()

    if args.outtype not in outtypes:
        exit("Error! Output type not recognized. Choose from %s" % outtypes)
        
    if not os.path.isfile(args.inputfile):
        exit("Error! Input file not found.")
    
    # Read
    intypes = ['dx', 'uv', 'DATA']
    if '.dx' in args.inputfile:
        print "Reading OpenDX input"
        #Contains only one distribution
        mygrids = {'.' : grid.dx2Grid(args.inputfile)}
        
    elif args.inputfile[-2:] == 'uv':
        print "Reading TINKER xuv input"
        ## Temporarily try 2.7+/3.0+
        #my = {key: value for (key, value) in sequence}
        # Using Python 2.6 compatible "dictionary comprehension"
        mygrids = dict(('%d.' % (i+1), mygrid) for (i, mygrid) in \
            enumerate(grid.TKRguv2Grids(args.inputfile)))

    elif "DATA" in args.inputfile:
        print "Reading UxDATA input"
        mygrids = grid.data2Grids(args.inputfile) # Already a dictionary
        for key in mygrids.keys():
            # Modify keys to be used as output filenames
            mygrids['%s.' % key] = mygrids.pop(key)

    elif ".uv.h5" in args.inputfile:
        print "Reading MDF .h5 input"
    
        mygrids = {}
        for speciesname, dictofgrids in grid.h5ToGrids(args.inputfile).iteritems():
            for disttype, mygrid in dictofgrids.iteritems():
                mygrids["%s.%s." % (speciesname, disttype)] = mygrid
            
    # Write
    if args.outtype == 'dx':
        print "Outputting .dx file(s)"
        for key, mygrid in mygrids.iteritems():
            mygrid.writedx('%sdx' % key)
      
    elif args.outtype == 'grd':
        print "Outputting Accelrys DS .grd file(s)"
        for key, mygrid in mygrids.iteritems():
            mygrid.writegrd('%sgrd' % key)
    

if __name__ == '__main__':
    main()

