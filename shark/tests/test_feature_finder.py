'''Test the the features loaded in feature_finder.py. If you add any new ones, you should add a test.'''
import pytest
import numpy as np
from shark import feature_finder as ff
from astropy.utils.data import get_pkg_data_filename

lc = get_pkg_data_filename("data/lc.txt")
x, y = np.loadtxt('data/lc.txt',skiprows=1,delimiter=',').T
s = ff.target(x, y, 'test')

def test_median():
    ans = s.median()
    assert np.isclose(ans, 100.245000089, 1E-3)

def test_std():
    ans = s.std()
    assert np.isclose(ans, 1.03635074413, 1E-3)

def test_diff():
    ans = s.diff()
    assert np.isclose(ans, 4.66157683728, 1E-3)

def test_flux_ratio():
    ans = s.flux_ratio()
    assert np.isclose(ans, -3.8531078532, 1E-3)

def test_flux_mid50():
    ans = s.flux_mid50()
    assert np.isclose(ans, 0.630701457106, 1E-3)

def test_flux_mid80():
    ans = s.flux_mid80()
    assert np.isclose(ans, 0.855224929257, 1E-3)

def test_perc_amp():
    ans = s.perc_amp()
    assert np.isclose(ans, 1.01673671082, 1E-3)

def test_mstat():
    ans = s.mstat()
    assert np.isclose(ans, -0.383868522527, 1E-3)

def test_grad_groups():
    ans = s.grad_groups()
    assert np.isclose(ans, 0, 1E-3)

def test_ngroups():
    ans = s.ngroups()
    assert np.isclose(ans, 0, 1E-3)

def test_ngauss():
    ans = s.ngauss()
    assert ans == 1

def test_dgauss():
    ans = s.dgauss()
    assert np.isclose(ans, 0.4493107, 1E-3)

def test_compute():
    s.compute(['median','std'])
    assert list(s.features.keys()) == ['median','std']
    assert np.isclose(s.features.loc[0, 'median'], 100.245, 1E-3)
    assert np.isclose(s.features.loc[0, 'std'], 1.036351, 1E-3)

    s.compute(['median','std'],['vanilla','clip'])
    assert len(s.features.keys()) == 4
