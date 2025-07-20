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
        clu_var = math.radians(kwargs.get('clu_var', 15))
        self.gens = [[]]
        self.root = Node(pos, None, 0, 0, 0, par_var, sib_var, clu_var, self.gens[0])
        
        

class Node:
    def __init__(self, pos, par, ang, gen, par_var, sib_var, clu_var, population):
        self.position = pos
        self.parent = par
        self.angle = ang
        self.children = []
        self.generation = gen
        self.guiding = 0
        self.parent_variance = par_var
        self.sibling_variance = sib_var
        self.cluster_variance = clu_var
        self.population = population
        self.population.append(self)
    
    def make_child(self):
        

        cousin_angle = 0

        cluster_angle = self.guiding
        density = density_func(self, self.population)

        bearing = to_unit(arr_sum(rand_arr, density_arr, cousin_arr, cluster_arr)) # + random.random()
        child_count = 2
        for i in child_count:
            rand_angle = random.random() * 2 * math.pi
            rand_arr = [math.cos(rand_angle), math.sin(rand_angle)]
            density_angle = random.random() * 2 * math.pi
            density_arr = to_unit(arr_sum(scale_arr([math.cos(self.angle), math.sin(self.angle)], density), [math.cos(density_angle), math.sin(density_angle)]))
            
            cousin_arr = [math.cos(cousin_angle), math.sin(cousin_angle)]
            cluster_arr = [math.cos(cluster_angle), math.sin(cluster_angle)]
            self.children.append(Node(arr_sum(self.pos, bearing), self, math.atan2(bearing[1], bearing[0]), self.generation + 1, self.par_var, self.sib_var))

def arr_sum(*args):
    output = [0, 0]
    for arg in args:
        output[0] += arg[0]
        output[1] += arg[1]
    return output

def arr_dif(arrA, arrB):
    output = []
    for i in len(arrA):
        output.append(arrA[i] - arrB[i])
    return output

def to_unit(arr):
    scale = get_scale(arr)
    if scale < 0.0001:
        return 0
    output = []
    for i in len(arr):
        output.append(arr[i] / scale)
    return output

def get_scale(arr):
    scale = 0
    for i in arr:
        scale += i * i
    return scale

def scale_arr(arr, scale):
    output = []
    for i in arr:
        output.append(i * scale)
    return output

def density_func(s, pop):
    count = 0
    for cousin in pop:
        if get_scale(arr_dif(s.position, cousin.position)) <= 1:
            count += 1
    return count


# Models to recreate:
# Density repulsion
# Cousin repulsion
# Clustering
# True Random