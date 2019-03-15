
""" photometryMaker is a package to be used in conjuction with funcMaker, to gather photometric magnitudes from
spectral data"""

import astropy
import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
from TransferFunctions.TransferGenerator import TransmissionFunction
C = 3e9 #speed of light, to be written in proper units

def _get_f_nu (spectra , Transmission):
    #integrate flux(x)*transmission(x)dx
    I1 = quad(lambda x : spectra(x)*Transmission(x)*x**3 ,Transmission.min, Transmission.max)
    I2 = quad(lambda x : Transmission * x , Transmission.min, Transmission.max)
    return I1/(C * I2)

def getABmag (spectra , Transmission):
    return -2.5*np.log10(_get_f_nu(spectra, Transmission)) - 48.6 #subtract 48.6 as zero mag reference

class spectralflux(TransmissionFunction):

    def __init__ (self, wave, flux):
        super(spectralflux, self).__init__(wave, flux)

    def __call__(self, wavelen):
        if type(wavelen) in [int, float]:
            if not self.min<wavelen<self.max:
                raise RuntimeError('Can\'t extrapolate spectral data')
            return self.f(wavelen)
        
        return [self.__call__(x) for x in wavelen]

    

