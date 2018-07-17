'''
TakeObs.py

Takes time series spectral observations.
'''
__author__ = 'Melissa Morris'
import seabreeze.spectrometers as sb
import matplotlib.pyplot as plt
from time import time
import numpy as np
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--save','-s',action='store',default=False,help='specify the base file name in which data will be saved')
parser.add_argument('--noplot','-p',action='store_true',default=False,help='get rid of live updating plot')
parser.add_argument('--integrationtime','-i',action='store',default=3000,help='specify integration time (in microseconds) of each spectrum')
parser.add_argument('--observationtime','-t',action='store',default=.1,help='specify total observation time in seconds')
args = parser.parse_args()

# Define spectrometer devices
devices = sb.list_devices()
spec = sb.Spectrometer(devices[0])

# Integration time
#spec.integration_time_micros(args.integrationtime)
spec.integration_time_micros(float(args.integrationtime))

# Define initial wavelengths and intensities
wlen = np.array(spec.wavelengths())
filt=np.where((wlen>=325)&(wlen<=475))
wlen=wlen[filt]
inten = spec.intensities()[filt]

# Create plot of Intensity vs. Wavelength
if not args.noplot:
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    spectre = ax.plot(wlen,inten)[0]
    plt.ylim(0,4500)
    plt.title("Device: " + spec.model + ", sn: " + spec.serial_number)
    plt.ylabel('intensity')
    plt.xlabel('wavelengths (nm)')

# Specify base name of data file
if args.save:
    basename = args.save
    f = open(basename,'w')
    observation_time = datetime.datetime.utcnow()
    strwlen = ','.join([str(i) for i in wlen])
    f.write('UTC Time: '+str(observation_time)+'\nTime,'+strwlen)
    f.close()
    f = open(basename,'a')

plotting = 0
t0 = time()
t1 = time()

# Creates a live updating plot for a specified observation time
                # How can we make this go until we turn it off?
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
    
    
    plotting += 1
    t1 = time()

if args.save:
    f.close()

spec.close()