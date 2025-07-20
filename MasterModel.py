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
        par_var = math.radians(kwargs.get('par_var', 15))
        sib_var = math.radians(kwargs.get('sib_var', 15))
        self.root = Node(pos, None, 0, 0, 0, par_var, sib_var)
        

class Node:
    def __init__(self, pos, par, ang, gen, par_var, sib_var):
        self.position = pos
        self.parent = par
        self.angle = ang
        self.children = []
        self.generation = gen
        self.guiding = 0
        self.parent_variance = par_var
        self.sibling_variance = sib_var
    
    def make_child(self):
        rand_angle = 0
        density_angle = 0
        cousin_angle = 0
        cluster_angle = 0
        angle = to_unit(arr_sum(rand_angle, density_angle, cousin_angle, cluster_angle)) # + random.random()
        self.children.append(arr_sum(self.pos, [math.cos(angle), math.sin(angle)], self, angle, self.generation + 1, self.par_var, self.sib_var))

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