import numpy as np
import matplotlib.pyplot as plt3323334
from glob import glob

basename = 'someobs'
flist = glob(basename+'/flat*')

i = 76

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#plt.title('No Filter (Saturates Easily)')
#plt.ylim(0,4500)
plt.xlim(390,410)
plt.ylabel('intensity')
plt.xlabel('wavelengths (nm)')
dat = np.loadtxt(flist[i],skiprows=2)
wlen = dat[:,0]
inten = dat[:,1]
ax.plot(wlen,inten)
plt.show()
#plt.savefig(basename+'_hnk.png')