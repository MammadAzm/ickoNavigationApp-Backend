from math import sin, cos, atan2, pi, sqrt
from .Constants import *


def distanceMeasure(lat1, lon1, lat2, lon2,):
    dlat = lat2*pi/180 - lat1*pi/180
    dlon = lon2*pi/180 - lon1*pi/180
    a = sin(dlat/2)**2 + cos(lat1*pi/180)*cos(lat2*pi/180)*sin(dlon/2)*sin(dlon/2)
    c = 2*atan2(sqrt(a), sqrt(1-a))
    distance = R*c
    return distance
