'''Create a gaussian mixture model object containing single numeric features.'''

import numpy as np
from sklearn.mixture import GaussianMixture

class gmm:
    '''
    Object that holds all the GMM information for a light curve
    '''
    def gauss(self,x,mean,sigma,weight):
        """A simple 1D Gaussian"""
        return weight*(2.*np.pi*sigma)**(-.5) * np.exp(-.5*(x-mean)**2./sigma)

    def make_gaussians(self,x,means,sigma2s,weights):
        """Add up a number of gaussians"""
        out = np.zeros_like(x)
        for i in np.arange(len(means)):
            out += self.gauss(x,means[i],sigma2s[i],weights[i])
        return out

    def __init__(self,y,nmax=5):
        obs = np.array([[i] for i in y])
        n_comps=np.arange(1,nmax)
        hold={}
        bic = np.array([])
        for n in n_comps:
                g = GaussianMixture(n_components=n)
                g.fit(obs)
                hold[n]=g
                k = np.float(3*n - 1.) #number of parameters
                nsamp = np.float(len(y))
                bic = np.append(bic,g.bic(obs))
        self.nbest = n_comps[np.argmin(bic)]
        g=hold[self.nbest]
        self.ngauss=len(g.means_.ravel()[g.weights_.ravel() > 1E-2])
        hist, bins= np.histogram(y,500,normed=True)
        self.x=(bins[:-1] + bins[1:]) / 2
        self.data=hist
        self.model=self.make_gaussians(self.x,g.means_.ravel(),g.covariances_.ravel(),g.weights_.ravel())
        self.stddev_gauss=np.std(hist-self.model)
        self.std_model=np.std(self.model)
        GMMsort=np.flipud(np.argsort(g.weights_.ravel()))
        self.GMMstd=(g.covariances_.ravel()[GMMsort][0])**0.5
        self.GMMmed=(g.means_.ravel()[GMMsort][0])
        self.cent_diffs=0
        if self.ngauss>=2:
            self.cent_diffs=(g.means_.ravel()[GMMsort][0])-(g.means_.ravel()[GMMsort][1])
        self.dmax=np.max(self.model)-np.min(self.model)
