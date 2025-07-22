import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color
import functools as ft
import igraph as ig

def zero_func(*args):
    return 0

def clamped(a, b, c):
    return (a > b) & (a < c)

def lerp(a, b, t):
    return a * (1 - t) + b * t

def get_angles(source, target, sRad, tRad, probability, rangeArr):
    d = distBetween(source, target)
    l = (sRad * sRad - tRad * tRad + d * d) / (2 * d)
    h = math.sqrt(sRad*sRad-l*l)
    sharedX = l / d * (target[0]-source[0])
    sharedY = l / d * (target[1]-source[1])
    pmX = h / d * (target[1]-source[1])
    pmY = h / d * (target[0]-source[0])
    low = math.atan2(sharedY-pmY,sharedX+pmX)
    high = math.atan2(sharedY+pmY,sharedX-pmX)
    if high < low:
        rangeArr.append([-math.pi, high, probability])
        rangeArr.append([low, math.pi, probability])
    else:
        rangeArr.append([low, high, probability])

def distBetween(a, b):
    return get_scale(arr_dif(a, b))

class Simulation:
    def __init__(self, **kwargs):
        self.pos = kwargs.get('pos', [0,0])
        self.par_var = math.radians(kwargs.get('par_var', 15))
        self.sib_var = math.radians(kwargs.get('sib_var', 15))
        self.clu_var = math.radians(kwargs.get('clu_var', 15))
        self.gens = None
        self.root = None
        self.generation = 0
        self.included = [kwargs.get('random_walk', False),
                         kwargs.get('density', False),
                         kwargs.get('cloud', False),
                         kwargs.get('cluster', False)]
        self.weights = [kwargs.get('random_walk_weight', 1 if self.included[0] else 0),
                        kwargs.get('density_weight', 1 if self.included[1] else 0),
                        kwargs.get('cloud_weight', 1 if self.included[2] else 0),
                        kwargs.get('clustering_weight', 1 if self.included[3] else 0)]
        self.independent_siblings = kwargs.get('independent_siblings', False)
        self.run_params = None
        self.graph = None
        self.clusters = None
        self.print_method = kwargs.get('print style', 0)
        
    def initialize(self):
        self.gens = [[]]
        self.clusters = []
        # self.run_params = [self.par_var, self.sib_var, self.clu_var, self.gens]
        self.root = Node(self.pos, None, 0, 0, self.par_var, self.sib_var, self.clu_var, self.gens[0], self.weights, self.included)
        self.generation = 0
        self.graph = None
        
    def run_gen(self):
        next_gen = []
        num = len(self.gens[self.generation])
        edges = []
        for source_index in range(num):
            for target_index in range(source_index + 1, num):
                if get_scale(arr_dif(self.gens[self.generation][source_index].position, self.gens[self.generation][target_index].position)) < f_t(self.generation):
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
            print("Finished gen", self.generation)
            
    def plot_end(self, env):
        for node in self.gens[-1]:
            node.plot_end(env)
    
    def plot_path(self, env):
        for node in self.gens[0]:
            node.plot_path(env)
        

class Node:
    def __init__(self, pos, par, ang, gen, par_var, sib_var, clu_var, population, w, i):
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
        self.weights = w
        self.included = i
        
    def set_guiding_angle(self, angle):
        self.guiding = angle
    
    def make_children(self, next):
        density = density_func(self, self.population)
        rand_arr = [0,0]
        density_arr = [0,0]
        cloud_arr = [0,0]
        cluster_arr = [0,0]
        if self.included[0]:
            rand_angle = random.random() * 2 * math.pi
            rand_arr = [math.cos(rand_angle), math.sin(rand_angle)]
        if self.included[1]:
            density_angle = random.random() * 2 * math.pi
            density_arr = to_unit(arr_sum(scale_arr([math.cos(self.angle), math.sin(self.angle)], density), [math.cos(density_angle), math.sin(density_angle)]))
        if self.included[2]:
            true_region = [[-math.pi, math.pi, 1]]
            regions = []
            cousins = self.get_child_cousins()
            for degree in range(len(cousins)):
                r = radius(self.generation, degree)
                for cousin in cousins[degree]:
                    if clamped(distBetween(self.position, cousin.position), 1 - r, 1 + r):
                        get_angles(self.position, cousin.position, 1, r, 0.1, regions)
            for region in regions:
                j = 0
                while (j < len(true_region)) and (true_region[j][1] < region[1]):
                    if (region[0] < true_region[j][1]):
                        if region[0] <= true_region[j][0]:
                            true_region[j][2] *= region[2]
                            region[0] = true_region[j][1]
                        else:
                            upper = true_region[j][1]
                            true_region[j][1] = region[0]
                            true_region.insert(j + 1, [region[0], upper, true_region[j][2] * region[2]])
                            region[0] = upper
                            j += 1
                    j += 1
                if (j < len(true_region)) & (region[1] > region[0]):
                    if true_region[j][1] == region[1]:
                        true_region[j][2] *= region[2]
                    elif (region[0] > true_region[j][0]):
                        upper = true_region[j][1]
                        true_region[j][1] = region[1]
                        true_region.insert(j + 1, [region[1], upper, true_region[j][2]])
                        true_region[j][2] *= region[2]
            index = random.choices(range(len(true_region)), map(lambda x: x[2] * (x[1]- x[0]) / math.pi / 2, true_region))[0]
            cloud_angle = lerp(true_region[index][0], true_region[index][1], random.random())
            cloud_arr = [math.cos(cloud_angle), math.sin(cloud_angle)]
        if self.included[3]:
            cluster_angle = self.guiding + random.random() * 2 * self.cluster_variance - self.cluster_variance
            cluster_arr = [math.cos(cluster_angle), math.sin(cluster_angle)]
        child_count = 2
        delta = to_unit(arr_sum(scale_arr(rand_arr, self.weights[0]),
                                scale_arr(density_arr, self.weights[1]),
                                scale_arr(cloud_arr, self.weights[2]),
                                scale_arr(cluster_arr, self.weights[3])))
        for _ in range(child_count):
            bearing = math.atan2(delta[1], delta[0]) + random.random() * 2 * self.sibling_variance - self.sibling_variance
            self.children.append(Node(arr_sum(self.position, [math.cos(bearing), math.sin(bearing)]), self, bearing, self.generation + 1, self.parent_variance, self.sibling_variance, self.cluster_variance, next, self.weights, self.included))
            
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
            uncommon_ancestor = common_ancestor
            common_ancestor = common_ancestor.parent
            i += 1
        return cousins
    
    def get_child_cousins_helper(self, arr, index):
        if index == 1:
            for child in self.children:
                arr.append(child)
        else:
            for child in self.children:
                child.get_child_cousins_helper(arr, index - 1)
    
    def plot_end(self, env):
        env.plot([self.position[0]], [self.position[1]], 'o', color = (0, 0, 0, .1))

    def plot_path(self, env):
        for child in self.children:
            env.plot([self.position[0], child.position[0]], [self.position[1], child.position[1]], color = (0, 0, 0, .1))
            child.plot_path(env)
        if len(self.children) == 0:
            self.plot_end(env)

def arr_sum(*args):
    output = [0, 0]
    for arg in args:
        output[0] += arg[0]
        output[1] += arg[1]
    return output

def arr_dif(arrA, arrB):
    output = []
    for i in range(len(arrA)):
        output.append(arrA[i] - arrB[i])
    return output

def to_unit(arr):
    scale = get_scale(arr)
    if scale < 0.0001:
        return 0
    output = []
    for i in range(len(arr)):
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
            count += 1 / 4
    return count

def f_t(t):
    return 0.012 * (2 * t + 2 - 1) / (t + 1)

def radius(gen, degree):
    return 0.1

plot.figure(1, figsize = (6, 6))
plot.axis([-10, 10, -10, 10])
sim = Simulation(random_walk = True, density = True, cloud = True, cluster = True)
sim.initialize()
sim.run_gens(10)
sim.plot_path(plot)

plot.show()
# Models to recreate:
# Density repulsion
# Cloud repulsion
# Clustering
# True Random