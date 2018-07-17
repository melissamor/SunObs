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

# Extracts data from file
def getdata(name):
    # Open the first file and read the first two lines
    f=open(name,'r')
    obs = f.readline()
    wlen=f.readline()
    f.close()
    # Saves wavelengths from the second line
    wlen = np.array([float(i) for i in wlen.split(',')[1:]])
    obs_time = obs[12:]
    # Reads the rest of the data
    dat = np.loadtxt(name,skiprows=2,delimiter=',')
    # Saves time and flux data
    time = dat[:,0]
    allflux = dat[:,1:]
    return wlen,allflux,time,obs_time
'''
filename = '../testflat_observation_10-25-2017_1.dat'
flux,near_flux,comp_flux=[],[],[]

wlen,allinten,obs_sec,ot = getdata(filename)
print 'data retrieved'
# Convert seconds to local time
hour= float(ot[9:11])
minute= float(ot[12:14])
second= float(ot[15:])

lhour = hour-5
ltime = lhour+minute/60+second/3600

obs = np.divide(obs_sec,3600)
obs = np.add(obs,ltime)
print 'time conversion completed'

for inten in allinten:
    care = np.where((wlen>391)&(wlen<395))
    flux.append(sum(inten[care])/(len(wlen[care])))
    
    nocare = np.where((wlen>386)&(wlen<390))
    near_flux.append(sum(inten[nocare])/(len(wlen[nocare])))
    
    hocare = np.where(((wlen>399)&(wlen<401))|((wlen>388)&(wlen<390)))
    comp_flux.append(sum(inten[hocare])/(len(wlen[hocare])))

print 'flux acquired'
'''
plt.plot(obs,flux)
plt.plot(obs,near_flux)
plt.plot(obs,comp_flux)
plt.show()

nflux = np.divide(flux,near_flux)
plt.plot(obs,nflux)
plt.show()

hnflux = pan.rolling_median(nflux,1000)
plt.plot(obs,h1h)
plt.show()

'''   
# Fit resulting light curve to polynomial
a=np.polyfit(obs,flux,10)
b=np.poly1d(a)
# Divide light curve by fitted polynomial
pflux = np.divide(flux,b(obs))

# Fit resulting light curve to polynomial
aa=np.polyfit(obs,comp_flux,10)
bb=np.poly1d(aa)
# Divide light curve by fitted polynomial
far_pflux = np.divide(comp_flux,bb(obs))

plt.plot(obs,flux)
plt.plot(obs,b(obs))
plt.plot(obs,comp_flux)
plt.plot(obs,bb(obs))
plt.show()

flat_flux_fun = np.divide(np.subtract(pflux,far_pflux),np.add(pflux,far_pflux))
plt.plot(obs,flat_flux_fun)
plt.show()

h1h = pan.rolling_median(flat_flux_fun,5000)
plt.plot(obs,h1h)
plt.title('Observation: '+ot)
plt.xlabel('Local Time')
plt.ylabel('Flux')
plt.savefig(filename[:-3]+'png')'''

