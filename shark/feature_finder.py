'''Feature finder for light curves

This is a database of features you might want to call on your light curves.
This is not a complete list and you can add your own. Given a list of features shark will find them on a given light curve.

Features MUST output a single, numeric value
'''

import numpy as np
from scipy.stats import skew,kurtosis
import pandas as pd
from . import events as ev
from .gmm import gmm

class target:
    '''A single target. Should have an x and y and some identifier'''

    def __init__(self, x, y, indentifier, ra = None, dec = None):
        '''Initialise shark object'''
        self.x = x
        self.y = y
        self.name = indentifier
        self.fin = np.isfinite(y)
        self.x_sort = x[np.argsort(y)]
        self.y_sort = np.sort(y)
        self.npoints = len(y)
        self.gy = np.gradient(self.y)
        self.features = pd.DataFrame()
        self.feature_list = {'median' : self.median,
                        'std' : self.std,
                        'diff' : self.diff}
        self.mode_list = {'vanilla' : self.vanilla,
                          'clip' : self.clip}

    #Tools to clean light curves
    #------------------------------------#
    def vanilla(self):
        return

    def clip(self, nstd = 6):
        '''Clip out nstd sigma outliers'''
        std = np.nanstd(self.y)
        self.y[np.abs(self.y-np.nanmedian(self.y)) > 6*std] = np.nan
    #------------------------------------#

    #Features
    #------------------------------------#
    def median(self):
        '''Return median y value'''
        return np.nanmedian(self.y)

    def std(self):
        '''Return standard deviation of y value'''
        return np.nanstd(self.y)

    def diff(self):
        '''Return the difference between the maximum and minimum value'''
        return np.nanmax(self.y)-np.nanmin(self.y)

    def flux_ratio(self):
        '''Return the difference between the median flux at the top 5% and the median flux at the bottom 5%'''
        return np.nanmedian(self.y_sort[0:self.npoints//20])-np.nanmedian(self.y_sort[-self.npoints//20:])

    def flux_mid20(self):
        '''Return the ratio of the median flux at the top 40% and the median flux at the bottom 40%, divided by the flux ratio.'''
        f1 = self.flux_ratio()
        flux_mid20 = np.nanmedian(self.y_sort[0:2*self.npoints//5])-np.nanmedian(self.y_sort[-2*self.npoints//5:])
        return flux_mid20/f1

    def flux_mid50(self):
        '''Return the ratio of the median flux at the top 25% and the median flux at the bottom 25%, divided by the flux ratio.'''
        f1 = self.flux_ratio()
        flux_mid50 = np.nanmedian(self.y_sort[0:self.npoints//4])-np.nanmedian(self.y_sort[-self.npoints//4:])
        return flux_mid50/f1

    def flux_mid80(self):
        '''Return the ratio of the median flux at the top 10% and the median flux at the bottom 10%, divided by the flux ratio.'''
        f1 = self.flux_ratio()
        flux_mid80 = np.nanmedian(self.y_sort[0:self.npoints//10])-np.nanmedian(self.y_sort[-self.npoints//10:])
        return flux_mid80/f1

    def perc_amp(self):
        '''Return the percentage amplitude. Maximum of the data divided by the median.'''
        return np.nanmax(self.y)/self.median()

    def mstat(self):
        '''Return the M-statistic'''
        m1 = np.nanmean(self.y_sort[0:self.npoints//10]-self.median())/self.std()
        m2 = np.nanmean(self.y_sort[-self.npoints//10:]-self.median())/self.std()
        M = (m1 + m2)/2.
        return M

    def skew(self):
        '''Return the skew'''
        return skew(self.y)

    def kurtosis(self):
        '''Return the kurtosis'''
        return kurtosis(self.y)

    def med_abs_dev(self):
        '''Return median absolute deviation'''
        return np.median(np.abs(self.y-self.median()))

    def dtav(self):
        '''Return the mean minus the median'''
        return np.mean(self.y)-np.median(self.y)

    def max_slope(self):
        '''Return the maximum slope in the data:
            max(y[1:] - y[0:-1])'''
        return np.nanmax(self.y_sort[1:]-self.y_sort[0:-1])

    def jack(self):
        '''Return the ratio of the standard deviation of the first half of the data to the standard deviation of the last half.'''
        return np.nanstd(self.y[0:self.npoints//2])/np.nanstd(self.y[self.npoints//2:])

    def slope(self):
        '''Return the slope of the data from a 1D polynomial fit'''
        line=np.polyfit(self.x[self.fin],self.y[self.fin],1)
        return line[1]

    def grad_std(self):
        '''Standard deviation of the gradient'''
        return np.nanstd(self.gy-np.nanmedian(self.gy))

    def grad_diff(self):
        '''Maximum of the gradient less the minimum of the gradient'''
        return np.nanmax(self.gy)-np.nanmin(self.gy)

    def grad_groups(self):
        '''Return the number of groups of points at least 3 sigma from the mean of the gradient. A group is defined as at least 3 points.'''
        f1=ev.find_events(self.x, self.gy, self.grad_std()*3)
        f2=ev.find_events(self.x, -self.gy, self.grad_std()*3)
        return(f1['ngroups']+f2['ngroups'])

    def run_events(self):
        '''Check whether to run the events finder'''
        if not hasattr(self, 'events'):
            self.events = ev.find_events(self.x, self.y, 3*self.std(), med=self.median())

    def ngroups(self):
        '''Return the number of groups of points at least 3 sigma from the mean. A group is defined as at least 3 points.'''
        self.run_events()
        return self.events['ngroups']

    def duty(self):
        '''Returns the duty cycle of events'''
        self.run_events()
        return self.events['duty']

    def medh(self):
        '''Returns the median height of events'''
        self.run_events()
        return self.events['medh']

    def medh_top(self):
        '''Returns the median height of the top 5 events'''
        self.run_events()
        return self.events['medh_top']

    def medl(self):
        '''Returns the median duration of events'''
        self.run_events()
        return self.events['medl']

    def dh(self):
        '''Returns the maximum height of events less the minimum height'''
        self.run_events()
        return self.events['dh']

    def dl(self):
        '''Returns the maximum duration of events less the minimum duration'''
        self.run_events()
        return self.events['dl']

    def run_gmm(self):
        '''Check whether to run the events finder'''
        if not hasattr(self, 'gmm'):
            self.gmm = gmm(self.y)

    def ngauss(self):
        '''Optimal number of Gaussians to describe population'''
        self.run_gmm()
        return self.gmm.ngauss

    def dgauss(self):
        '''Standard deviation of residuals between GMM and data'''
        self.run_gmm()
        return self.gmm.stddev_gauss

    def std_gauss(self):
        '''Standard deviation of GMM model'''
        self.run_gmm()
        return self.gmm.std_model

    def cleanup(self):
        '''Remove added attributes'''
        if not hasattr(self, 'events'):
            del self.events
        if not hasattr(self, 'gmm'):
            del self.gmm


    def compute(self, user_features, user_modes=['vanilla']):
        '''Compute a list of features. Example:
            s = target(x, y, 'TARGNAME')
            s.compute(['median', 'std', 'mean', 'dtav', 'perc_amp'])

        s gains attribute 'features' which contains a dataframe of the input features.

        Use 'mode' to specify what version of the light curve to run on. This will be done iteratively.

        e.g. the following command will find the median and the standard deviation on the raw light curve and on the clipped light curve.

            s.compute(['median', 'std'], mode=['vanilla','clipped'])
        '''
        #Check the inputs are iterable.
        if not hasattr(user_features,"__iter__"):
            user_list = [user_features]
        if not hasattr(user_modes,"__iter__"):
            user_list = [user_modes]

        for mode in user_modes:
            if mode in self.mode_list.keys():
                self.cleanup()
                self.mode_list[mode]()
            else:
                continue
            if (mode == 'vanilla') or (len(user_modes) == 0):
                prf = ''
            else:
                prf = '{}_'.format(mode)

            for feature in user_features:
                if feature in self.feature_list.keys():
                    self.features.loc[0,'{}{}'.format(prf, feature)] = (self.feature_list[feature]())

    #------------------------------------#
