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
        self.pos = kwargs.get('pos', [0,0])
        self.par_var = math.radians(kwargs.get('par_var', 15))
        self.sib_var = math.radians(kwargs.get('sib_var', 15))
        self.clu_var = math.radians(kwargs.get('clu_var', 15))
        self.gens = None
        self.root = None
        self.generation = 0
        self.included = [kwargs.get('random walk', False),
                         kwargs.get('density', False),
                         kwargs.get('cloud', False),
                         kwargs.get('clustering', False)]
        self.weights = [kwargs.get('random walk weight', 1 if self.included[0] else 0),
                        kwargs.get('density weight', 1 if self.included[1] else 0),
                        kwargs.get('cloud weight', 1 if self.included[2] else 0),
                        kwargs.get('clustering weight', 1 if self.included[3] else 0)]
        self.independent_siblings = kwargs.get('independent_siblings', False)
        self.run_params = None
        self.graph = None
        self.clusters = None
        self.print_method = kwargs.get('print style', 0)
        
    def initialize(self):
        self.gens = [[]]
        self.clusters = []
        # self.run_params = [self.par_var, self.sib_var, self.clu_var, self.gens]
        self.root = Node(self.pos, None, 0, 0, 0, self.par_var, self.sib_var, self.clu_var, self.gens[0])
        self.generation = 0
        self.graph = None
        
    def run_gen(self):
        next_gen = []
        num = len(self.gens[self.generation])
        edges = []
        for source_index in range(num):
            for target_index in range(source_index + 1, num):
                if get_scale(arr_dif(self.gens[self.generation][source_index], self.gens[self.generation][target_index])) < f_t(self.generation):
                    edges.append([source_index, target_index])
        g = ig.Graph(num, edges)
        components = g.connected_components(mode='weak')
        self.clusters.append(len(components))
        angles = []
        
        for _ in components:
            angles.append(random.random() * 2 * math.pi)
        
        for index, component in enumerate(components):
            for node in component:
                self.gens[self.generation][node].set_guiding_angle(angles[index])
        
        for node in self.gens[self.generation]:
            node.make_children(next_gen)
        
        self.generation += 1
        self.gens.append(next_gen)
        
    def run_gens(self, num):
        for i in range(num):
            self.run_gen()
        

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
        
    def set_guiding_angle(self, angle):
        self.guiding = angle
    
    def make_child(self, next):
        
        density = density_func(self, self.population)
        rand_angle = random.random() * 2 * math.pi
        rand_arr = [math.cos(rand_angle), math.sin(rand_angle)]
        density_angle = random.random() * 2 * math.pi
        density_arr = to_unit(arr_sum(scale_arr([math.cos(self.angle), math.sin(self.angle)], density), [math.cos(density_angle), math.sin(density_angle)]))
        bounds = [-math.pi, math.pi]
        adherance = [1]
        cousins = self.get_child_cousins()
        for degree in range(len(cousins)):
            r = radius(self.generation, degree)
            for cousin in cousins[degree]:
                

        cloud_angle = random.choices()
        cloud_arr = [math.cos(cloud_angle), math.sin(cloud_angle)]
        cluster_angle = self.guiding_angle + random.random * 2 * self.guiding - self.guiding
        cluster_arr = [math.cos(cluster_angle), math.sin(cluster_angle)]
        child_count = 2
        for _ in range(child_count):
            delta = to_unit(arr_sum(rand_arr, density_arr, cloud_arr, cluster_arr)) 
            bearing = math.atan2(delta[1], delta[0]) + random.random * 2 * self.sibling_variance - self.sibling_variance
            self.children.append(Node(arr_sum(self.pos, [math.cos(bearing), math.sin(bearing)]), self, bearing, self.generation + 1, self.parent_variance, self.sibling_variance, self.cluster_variance, next))
            
    def get_child_cousins(self):
        cousins = [[]]
        uncommon_ancestor = self
        common_ancestor = self.parent
        i = 1
        while common_ancestor is not None:
            cousins.append([])
            for cousin in common_ancestor.children:
                if cousin is not uncommon_ancestor:
                    cousin.get_child_cousins_helper(cousins[i], i)
            i += 1
        return cousins
    
    def get_child_cousins_helper(self, arr, index):
        if index == 1:
            for child in self.children:
                arr.append(child)
        else:
            for child in self.children:
                child.get_child_cousins_helper(arr, index - 1)

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
    return math.sqrt(scale)

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

def f_t(t):
    return 0.025 * (2 * t + 1) / (t + 1)

def radius(gen, degree):
    return 0.1


# Models to recreate:
# Density repulsion
# Cloud repulsion
# Clustering
# True Random