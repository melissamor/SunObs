'''
Data Reduction:
    
1. read the spectra from each file
2. save the wavelength range that we care about (H&K lines and part of the spectrum above and below that)
3. get rid of the noise from the surrounding regions by dividing by light curve of nearby region
4. divide by fitted polynomial to get rid of leftover noise
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pan

def getwlen(name):
    # Open the first file and read the first two lines
    f=open(name,'r')
    obs = f.readline()
    wlen=f.readline()
    f.close()
    # Saves wavelengths from the second line
    wlen = np.array([float(i) for i in wlen.split(',')[1:]])
    return wlen


# Extracts data from file
def getdata(name):
    # Open the first file and read the first two lines
    #f=open(name,'r')
    #obs = f.readline()
    #wlen=f.readline()
    #f.close()
    # Saves wavelengths from the second line
    #wlen = np.array([float(i) for i in wlen.split(',')[1:]])
    #obs_time = obs[12:]
    # Reads the rest of the data
    dat = np.loadtxt(name,delimiter=',')
    # Saves time and flux data
    #time = dat[:,0]
    allflux = dat[:,:]
    return allflux#,time,obs_time

filename = '../testflat_observation_10-24-2017_1.dat'
flux,near_flux,comp_flux=[],[],[]

wlen = getwlen(filename)
print 'wlen retrieved'
allinten= getdata(filename)
print 'intensities retrieved'

for q,inten in enumerate(allinten):
    care = np.where((wlen>391)&(wlen<395))
    flux.append(sum(inten[care])/(len(wlen[care])))
    
    nocare = np.where((wlen>386)&(wlen<390))
    near_flux.append(sum(inten[nocare])/(len(wlen[nocare])))
    
    hocare = np.where(((wlen>399)&(wlen<401))|((wlen>388)&(wlen<390)))
    comp_flux.append(sum(inten[hocare])/(len(wlen[hocare])))
    print str(q)+'/'+str(len(allinten))
    
print 'light curves made'


plt.plot(range(len(flux)-1),flux)
plt.show()
