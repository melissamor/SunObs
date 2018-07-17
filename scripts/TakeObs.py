'''
TakeObs.py

Takes time series spectral observations.

Syntax with optional arguments:
python TakeObs.py -s [path to output data] -p (only use if you do not want a live updating plot) -i [integration time in microseconds] -t [total observation time in seconds]
'''
__author__ = 'Melissa Morris'
# More info on seabreeze module: https://github.com/ap--/python-seabreeze
import seabreeze.spectrometers as sb
import matplotlib.pyplot as plt
from time import time
import numpy as np
import datetime
import argparse
from glob import glob

# Lists all possible arguments and what their purpose is
parser = argparse.ArgumentParser()
parser.add_argument('--save','-s',action='store',default=False,help='specify the base file name in which data will be saved')
parser.add_argument('--noplot','-p',action='store_true',default=False,help='get rid of live updating plot')
parser.add_argument('--integrationtime','-i',action='store',default=3000,help='specify integration time (in microseconds) of each spectrum')
parser.add_argument('--observationtime','-t',action='store',default=.1,help='specify total observation time in seconds')
args = parser.parse_args()

# Define spectrometer devices
devices = sb.list_devices()
spec = sb.Spectrometer(devices[0])

# Set integration time
spec.integration_time_micros(float(args.integrationtime))

# Define initial wavelengths and intensities
wlen = np.array(spec.wavelengths())
filt = np.where((wlen>=325)&(wlen<=475))
wlen = wlen[filt]
inten = spec.intensities()[filt]

# Create plot of Intensity vs. Wavelength
if not args.noplot:
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    spectre = ax.plot(wlen,inten)[0]
    plt.plot([320,480],[4000]*2,'r')
    plt.xlim(320,480)
    plt.ylim(0,4500)
    plt.title("Device: " + spec.model + ", sn: " + spec.serial_number)
    plt.ylabel('intensity')
    plt.xlabel('wavelengths (nm)')

# Begins to write file and saves header
if args.save:
    basename = args.save
    # If a file with the spedified name exists, raises an error and stops running the program
    if basename in glob(basename):
        raise ValueError('This file already exists. Delete it or save data to a different file.')
    # Creates file
    f = open(basename,'w')
    observation_time = datetime.datetime.utcnow()   # Current date and time
    strwlen = ','.join([str(i) for i in wlen])  # Creates a string that is every wavelength separated by commas
    # Write header to file
    f.write('UTC Time: '+str(observation_time)+'\nExposure Time: '+str(args.integrationtime)+'\nTime,'+strwlen)
    f.close()
    # Open file in append mode in order to add data to it
    f = open(basename,'a')

plotting = 0
t0 = time()
t1 = time()

# Creates a live updating plot for a specified observation time
try:
    while t1-t0 < float(args.observationtime):
        # Takes data
        inten = spec.intensities()
        inten = inten[filt]
        
        # if specified, saves spectrum to file
        if args.save:
            f.write('\n'+str(t1-t0)+','+(','.join([str(i) for i in inten])))
        
        # Updates plot with current data
        if not args.noplot:
            spectre.set_ydata(inten)
            plt.draw()
            plt.pause(.0001)
        
        # Updates time
        plotting += 1
        t1 = time()

    if args.save:
        f.close()
    
    spec.close()

# If the code is ended with a keyboard interrupt, closes spectrometer and files
# *** Not entirely sure that this is working properly
except KeyboardInterrupt:
    if args.save:
        f.close()
    spec.close()
except:
    raise