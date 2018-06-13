'''
ViewSpect.py

Plots a single spectrum of choice from dataset.

Syntax: python ViewSpect.py [path to data file] [index of spectrum you wish to plot]
'''

import numpy as np
import matplotlib.pyplot as plt
from sys import argv

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

# basename = argv[1]
basename = '../data/sun20180320_1.dat'
wlen,allflux,time,obs_time = getdata(basename)

hour= float(obs_time[9:11])
minute= float(obs_time[12:14])
second= float(obs_time[15:])
lhour = hour-5
ltime = lhour+minute/60+second/3600
obs = np.divide(time,3600)
obs = np.add(time,ltime)

# i = argv[2]
i = 10

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#plt.ylim(500,700)
#plt.xlim(325,470)
plt.ylabel('intensity')
plt.xlabel('wavelengths (nm)')
ax.plot(wlen,allflux[i])
plt.show()
#plt.savefig(basename+'_hnk.png')
