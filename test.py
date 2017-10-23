import numpy as np

name = '../someobs.dat'

fil = open(name,'r')
one = fil.readline()
two = fil.readline()
fil.close()
dat = np.loadtxt(name,skiprows=2,delimiter=',')
w = np.array([float(i) for i in two.split(',')[1:]])
f = dat[:,1:]

print(len(f[0]))
print(len(w))

'''
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

'''