'''
Data Reduction:
    
1. read the spectra from each file
2. save the wavelength range that we care about (H&K lines and part of the spectrum above and below that)
3. get rid of the noise from the surrounding regions (perhaps plot all of them together to see what it looks like)
4. plot the variation as a function of time to search for any sources of variability
5. search for variability?
    - set a baseline flux and say that if it raises above some x flux, it's a flare?
    - search for a periodic variability? (fourier transforms?)
    - some other way of looking for variability that I'm not sure about?
'''

import numpy as np
import matplotlib.pyplot as plt

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

filename = 'tenminobs.dat'
avint,navint,havint=[],[],[]

wlen,allinten,obs,ot = getdata(filename)

for inten in allinten:
    care = np.where((wlen>391)&(wlen<395))
    #care = np.where((wlen>420)&(wlen<430))
    avint.append(sum(inten[care])/(len(wlen[care])))
    
    #nocare = np.where((wlen>400)&(wlen<405))
    nocare = np.where((wlen>386)&(wlen<390))
    navint.append(sum(inten[nocare])/(len(wlen[nocare])))
    
    hocare = np.where((wlen>420)&(wlen<430))
    havint.append(sum(inten[hocare])/(len(wlen[hocare])))

navint = np.multiply(np.median(avint)/np.median(navint),navint)
#havint = np.multiply(np.median(avint)/np.median(havint),havint)
#plt.plot(obs,havint)
#plt.xlim(1000,1040)
plt.plot(obs,avint,alpha=.7)
plt.plot(obs,navint,alpha=.7)
plt.show()

wellokay = np.divide(avint,navint)
#plt.xlim(1000,1040)
plt.plot(obs,wellokay)
plt.show()