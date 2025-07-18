import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color
import functools as ft
import igraph as ig

print(eval("2+2", {}, []))

def zero_func(*args):
    return 0

class Simulation:
    def __init__(self, **kwargs):
        pos = kwargs.get('pos', [0,0])
        var = math.radians(kwargs.get('var', 15))
        self.root = Node(pos, None, 0, 0, 0, var)
        

class Node:
    def __init__(self, pos, par, ang, gen, guide, var):
        self.position = pos
        self.parent = par
        self.angle = ang
        self.children = []
        self.generation = gen
        self.guiding = guide
        self.variance = var
    
    def make_child(self):
        return 0

def arr_sum(*args):
    output = [0, 0]
    for arg in args:
        output[0] += arg[0]
        output[1] += arg[1]
    return output

def to_unit(arr):
    scale = 0
    for i in arr:
        scale += i * i
    if scale < 0.0001:
        return 0
    output = []
    for i in len(arr):
        output.append(arr[i] / scale)
    return output


# Models to recreate:
# Density repulsion
# Cousin repulsion
# Clustering
# True Random