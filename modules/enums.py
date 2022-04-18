# Standard Packages
from enum import Enum


class ProfileType(Enum):
    '''Specifies the type of profiles that can be plotted'''
    NONE = 0
    INPUT = 1
    OUTPUT = 2
    COMPARED = 3
    ADDITIONAL = 4


class SaveType(Enum):
    '''Specifies the type of data being saved in a file'''
    NONE = 0
    INPUT = 1
    OUTPUT = 2
    ADDITIONAL = 3
    CONTROLS = 4
    OPTIONS = 5


class ScanType(Enum):
    '''Specifies the type of data being scanned'''
    NONE = 0
    VARIABLE = 1
    CONTROL = 2
    TIME = 3


class ShotType(Enum):
    '''Specifies the type of the shot in the referenced CDF'''
    NONE = 0
    NSTX = 1
    DIII_D = 2
    NSTX_U = 3
    MAST = 4


class MergeType(Enum):
    '''Specifies the type of PDF merge'''
    NONE = 0
    PROFILES = 1
    PROFILEFACTORS = 2
    FACTORS = 3
    RHOVALUES = 4
