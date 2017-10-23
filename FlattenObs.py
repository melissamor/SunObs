import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, UnivariateSpline

#TRY to find continuum points of a spectrum for flattening
def get_continuum_points(wvl, flux, rad=15.0, const=0.6, num=0.03, snum=20):
    wvl = np.asarray(wvl)
    flux = np.asarray(flux)
    
    #Declare lists to contain supposed continuum points.
    c_wvl, c_flux = [], []
    
    #Just for fun.
    tmp_w, tmp_f = [], []
    
    #Keep track of a stretch of points on the spectrum that might be continuum.
    #If there are a lot of continuum points in a row, only store one continuum
    #   point (either the max, or the median, or something).
    stretch_w, stretch_f = [], []

    #Go through the spectrum and make an approximate continuum
    # (Based on the standard deviation around absorption features).
    for w, f in zip(wvl, flux):
        mask = (wvl > w-rad) & (wvl < w+rad)
        #w_chunk = wvl[mask]
        f_chunk = flux[mask]
        cont_flux = np.mean(f_chunk)+const*np.std(f_chunk)
        if abs(cont_flux/f - 1) < num:
            stretch_w.append(w)
            stretch_f.append(f)
        else:
            if len(stretch_w) > 0 and len(stretch_w) >= snum:
                stretch_w, stretch_f = np.asarray(stretch_w), np.asarray(stretch_f)
                i = int(len(stretch_f)/1.2)
                sort = np.argsort(stretch_f)
                c_wvl.append(stretch_w[sort][i])
                c_flux.append(stretch_f[sort][i]) 
            stretch_w, stretch_f = [], []
        tmp_w.append(w)
        tmp_f.append(cont_flux)

    return c_wvl, c_flux
    
#A function for manually flattening a spectrum by selecting points on 
#   the continuum
def flatten(wvl, flux, guess_continuum=True, plot=True, Univariate=False):
    #Make a copy of the spectrum, so that the origonal is not changed
    wvl, flux = np.asarray(wvl).copy(), np.asarray(flux).copy()
    
    #Define empty lists to eventually contain the flattened spectrum.
    wvl_flat, flux_flat = [], []
        
    #Generate a figure and axes
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title("Flattening")
    ax.set_xlabel("Wavelength ($\AA$)")
    ax.set_ylabel("Flux")
    
    #Print instructions for flattening in the corner of the plot
    fig.text(0.52, 0.85, "'SPACEBAR' to place new continuum point.", fontsize=10)
    fig.text(0.52, 0.82, "'r' to remove nearest continuum point.", fontsize=10)
    fig.text(0.52, 0.79, "arrow keys to adjust nearest continuum point.", fontsize=10)
    fig.text(0.52, 0.76, "'q' to finish and divide spectrum by continuum.", fontsize=10)
    
    #Plot the spectrum to be flattened
    ax.plot(wvl, flux, lw=1)
    
    #Stop matplotlib from autoscaling the plot
    ax.autoscale(False)
    
    #Declare a list of continuum points
    if guess_continuum: wvl_points, flux_points = get_continuum_points(wvl, flux)
    else: wvl_points, flux_points = [], []
    
    #Plot the points as red dots
    points = ax.plot(wvl_points, flux_points, 'ro')[0]
    
    #Make a plot object which will eventually be the continuum fit
    # after there are enough points to generate a spline fit.
    continuum = ax.plot(wvl_points, flux_points)[0]
    
    #Disable some matplotlib default key commands
    if 'keymap.home' in plt.rcParams: plt.rcParams['keymap.home'].remove('r')
    if 'keymap.forward' in plt.rcParams: plt.rcParams['keymap.forward'].remove('right')
    if 'keymap.back' in plt.rcParams: plt.rcParams['keymap.back'].remove('left')
    
    #Declare the sensitivity of adjustments to continuum points
    # that can be made using the arrow keys.
    sens = 0.005
    
    
    def onclick(event, ax=ax):
        #Determine continuum point nearest to the cursor when click event occured.
        dists = []
        for x,y in zip(wvl_points, flux_points):
            dists.append((x - event.xdata)**2 + (y - event.ydata)**2)
        if len(dists) > 0:
            i = dists.index(min(dists))
        elif event.key != ' ':
            print "Cannot perform action."
            return
        
        #Determine size of the plot
        x_dist = abs(np.diff(ax.get_xlim())[0])
        y_dist = abs(np.diff(ax.get_ylim())[0])

        if event.key == ' ' and not (event.xdata == None or event.ydata == None):
            wvl_points.append(event.xdata)
            flux_points.append(event.ydata)
        elif event.key == 'n' and not (event.xdata == None or event.ydata == None):
            obs_dists = [(x-event.xdata)**2+(y-event.ydata)**2 for x,y in zip(wvl, flux)]
            o = obs_dists.index(min(obs_dists))
            wvl_points.append(float(wvl[o]))
            flux_points.append(float(flux[o]))
        elif event.key == 'r':
            wvl_points.pop(i)
            flux_points.pop(i)
        elif event.key == 'up':
            flux_points[i] += sens*y_dist
        elif event.key == 'down':
            flux_points[i] -= sens*y_dist
        elif event.key == 'right':
            wvl_points[i] += sens*x_dist
        elif event.key == 'left':
            wvl_points[i] -= sens*x_dist
        elif event.key == 'q':
            fig.canvas.mpl_disconnect(cid)
            mask = (wvl > min(wvl_points)) & (wvl < max(wvl_points))
            wvl_flat.extend(wvl[mask])
            print len(flux[mask]), len(continuum.get_ydata())
            flux_flat.extend(flux[mask]/continuum.get_ydata())
            if plot:
                fig_flat = plt.figure()
                ax_flat = fig_flat.add_subplot(1, 1, 1)
                ax_flat.plot(wvl_flat, flux_flat, color='black', lw=1)
            np.savetxt('wowthisiscool.dat',np.stack((continuum.get_xdata(),continuum.get_ydata()),axis=1))     
	    fig_flat.show()
            print hex(id(wvl_flat))
            return wvl_flat, flux_flat
        points.set_data(wvl_points, flux_points)
        if len(wvl_points) >= 4:
            if not Univariate:
                fit = interp1d(wvl_points, flux_points, kind='cubic')
                mask = (wvl > min(wvl_points)) & (wvl < max(wvl_points))
                continuum.set_data(wvl[mask], fit(wvl[mask]))
            else:
                fit = UnivariateSpline(wvl_points, flux_points, s=5e-5)
                continuum.set_data(wvl, fit(wvl))
        plt.draw()
        
    cid = fig.canvas.mpl_connect('key_press_event', onclick)
    print hex(id(wvl_flat))
    fig.show()
    return wvl_flat, flux_flat, continuum

def allflat(wvl,flux,cont):
    wvl_points = cont.get_xdata()
    mask = (wvl >= min(wvl_points)) & (wvl <= max(wvl_points))
    wvl_flat,flux_flat = [],[]
    wvl_flat.extend(wvl[mask])
    flux_flat.extend(flux[mask]/cont.get_ydata())
    return flux_flat,wvl_flat
    

#If this file is run as a script, do this:
if __name__ == '__main__':
    #Load the specified two-column lightcurve
    import sys
    name = sys.argv[1]
    exist = "no" #sys.argv[2]
    fil = open(name,'r')
    one = fil.readline()
    two = fil.readline()
    fil.close()
    dat = np.loadtxt(name,skiprows=2,delimiter=',')
    w = np.array([float(i) for i in two.split(',')[1:]])
    f = dat[:,1:]
    time = dat[:,0]

    if exist == "no":
        #Flatten it!
        w_flat, f_flat,cont = flatten(w, f[0])
        plt.show()
        
    fil = open('flattened_'+name,'w')
    fil.write(one)
    strwlen = ','.join([str(i) for i in w_flat])
    fil.write('Time,'+strwlen)
    fil.close()
    fil = open('flattened_'+name,'a')
    for j,i in enumerate(f):
        flux,wvl = allflat(w,i,cont)
        fil.write('\n'+str(time[j])+','+(','.join([str(ii) for ii in flux])))
    fil.close()
        