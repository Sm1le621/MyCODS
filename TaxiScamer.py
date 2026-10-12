import math
import time

def distance(t):
    BASETARIF = 4
    a = 0.25
    dist = float(t)* 1000
    v = round(((dist / 140)* a + BASETARIF), 2)
    return v

