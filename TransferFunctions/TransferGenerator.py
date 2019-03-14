#Generate Transfer function
import numpy as np
from scipy.interpolate import interp1d
import re

IGNORE = re.compile('#.+')
# Assumes data is formated as <wave_length> <transfer>\n
floats = lambda  x : [float(i) for i in x]


def load (filename):
    File = open(filename, 'r')
    data = list(filter(lambda x: not bool(IGNORE.match(x)), File.read().split('\n')))
    data = [floats(s.split()) for s in data]
    File.close()
    data = np.transpose(list(filter(lambda x : x != [], data)))
    return data[0], data[1] #wavelength, transmission

def reshape(prevdomain, trans, newdomain):
    f = interp1d(prevdomain, trans)
    return np.array(map(lambda x : 0 if not min(prevdomain)<x<max(prevdomain) else f(x) , newdomain))


class TransmissionFunction: 
    
    def __init__ (self, wave, trans):
        self.min = min(wave)
        self.max = max(wave)
        self.f = interp1d(wave, trans, kind='cubic')
        
    def __call__ (self, wavelen) :
        if type(wavelen) in [float, int]:
            return 0 if not self.min<wavelen< self.max else self.f(wavelen)
        
        return map(lambda x : 0 if not self.min<x< self.max else self.f(x) , wavelen)
    
    def __getstate__(self):
        return {'wave' : self.f.x,
        'trans': self.f.y}

    def __setstate__(self , state):
        self.__dict__.update({
            "min" : min(state['wave']),
            'max' : max(state['wave']),
            'f' : interp1d(state['wave'], state['trans'], kind='cubic')
        })
    