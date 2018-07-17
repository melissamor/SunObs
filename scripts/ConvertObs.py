'''
ConvertObs.py

Takes old spectral observations and condenses them into a single file.
'''

import numpy as np
from glob import glob

oldpath = glob('observation_1/obs*')
newpath = 'testobservation_1.dat'

f = open(oldpath[0],'r')
first = f.readline()
second = f.readline()
f.close()

observation_time = first[12:]

wlen = np.loadtxt(oldpath[0],skiprows = 2)[:,0]

f=open(newpath,'w')
strwlen = ','.join([str(i) for i in wlen])
f.write('UTC Time: '+str(observation_time)+'Time,'+strwlen)
f.close()

newf=open(newpath,'a')

for j,i in enumerate(oldpath):
    f = open(i,'r')
    one = f.readline()
    f.close()
    flux = np.loadtxt(i,skiprows=2)[:,1]
    newf.write('\n'+str(j)+','+(','.join([str(i) for i in flux])))