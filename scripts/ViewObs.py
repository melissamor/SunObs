import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from sys import argv

basename = argv[1]

f=open(basename,'r')
f.readline()
wlen=f.readline()
f.close()

wlen = np.array([float(i) for i in wlen.split(',')[1:]])

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.ylim(0,3000)
#plt.ylim(0,3)
plt.xlim(325,475)
plotdat = ax.plot(0,0)[0]

dat = np.loadtxt(basename,skiprows=2,delimiter=',')
time = dat[:,0]
inten = dat[:,1:]


for i,flu in enumerate(inten):
    plotdat.set_data(wlen,flu)
    plt.draw()
    plt.pause(.035)