import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color
import functools as ft

def distance(a, b):
    return math.sqrt(dist_squared(a, b))

def dist_squared(a, b):
    dist = 0
    for i, j in a, b:
        dist += (i - j) * (i - j)
    return dist

def arr_sum(first_arr, second_arr):
    output = []
    for i in range(len(first_arr)):
        output.append(first_arr[i] + second_arr[i])
    return output        

class Node:
    def __init__(self, pos, ang, gen, par, steps, pd, sd, a, dF, cF, rF, roF, slF):
        self.position = pos
        # 
        self.angle = ang
        # 
        self.generation = gen
        # 
        self.children = []
        # 
        self.parent = par
        # 
        self.count = 0
        # 
        self.step_len = steps
        # 
        self.parent_dev = pd
        # 
        self.sibling_dev = sd
        # 
        self.alpha = a
        # Weight cousin repulsion has on angle
        self.beta = 1 - a
        # Weight density has on angle
        self.density_func = dF
        # 
        self.count_func = cF
        # 
        self.radius_func = rF
        # 
        self.repulsion_odd_func = roF
        # 
        self.step_len_func = slF
        # 
    
    def give_birth(self):
        parent_population = 
        child_population = 
        density = self.density_func(self, self.generation, parent_population)
        self.count = self.count_func(self, self.generation, density, parent_population)
        
        direction = self.angle
        
        self.children.append(Node(arr_sum(self.position, [math.cos(), math.sin()])))
        
        for i in range(1, self.count):
            
        
def density(current, gen, population):
    output = 0
    for cousin_degree in population:
        for cousin in cousin_degree:
            if distance(current.position, cousin.position) < 1 :
                output += 1
    return output

def child_count_more_density(current, gen, density, population):
    if gen < 2:
        return 10
    return math.floor(2 + 3 / (1 + math.exp(-density)))

def child_count_less_density(current, gen, density, population):
    if gen < 2:
        return 10
    return math.floor(2 + 3 / (1 + math.exp(density)))

def radius(current, gen, density, removed, population):
    return 0.9**(gen * removed)

def radius_alt(current, gen, density, removed, population):
    return 0.9**(gen) * math.max(1, removed)

def radius_other(current, gen, density, removed, population):
    return 0.9**(removed) * math.max(1, gen)

def repulsion_odds(current, gen, density, removed, population):
    return 0

def step_length(current, gen, density, population):
    return 1

root = Node([0, 0], 0, 0, None, 1, 90, 10, 0.5, density, child_count_more_density, radius, repulsion_odds, step_length)

plot.show()