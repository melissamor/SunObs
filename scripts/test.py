import numpy as np

fname = '../testobservation_1.dat'

dat = np.loadtxt(fname,skiprows=2,delimiter=',')

for i in dat[15:20]:
    print len(i)