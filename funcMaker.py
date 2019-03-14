from TransferFunctions.TransferGenerator import load, TransmissionFunction
import sys
import pickle
import re
import os
import numpy as np
from functools import reduce
import ntpath


RET = re.compile('.+(?=[.])')
FILE = re.compile('.*[.]+')

def getFiles(name):
    if bool(FILE.match(name)):
        return name

    else:
        return [getFiles(str(name+'/'+x)) for x in os.listdir(name)]

def loadAll(path):
    return {ntpath.basename(f) : pickle.load(open(f, 'rb')) for f in flatten(getFiles(path))}


def flatten(l):
    return reduce(lambda x , y : x + flatten(y) if type(y) in [list, np.ndarray] else x + [y], l , list())

def main(args):
    dir_= ""
    for index,  name in enumerate(args):
        if name == '-f':
            dir_  = args[index+1]
            
        elif args[index-1] != '-f': 
            for f in flatten(getFiles(name)):
                T = TransmissionFunction(*load(f))
                with open(dir_+'/' + RET.findall(ntpath.basename(f))[0] + '.P', 'wb') as f:
                    pickle.dump(T, f, protocol = 2)

def _cmdMain():
    main(sys.argv[1:])       

if __name__ == '__main__':
    _cmdMain()
                 




