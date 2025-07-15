import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color
import functools as ft
import igraph as ig

def distSquared(a, b):
    output = 0
    for i in range(2):
        output += (a[i] - b[i]) * (a[i] - b[i])
    return output

def distReg(a,b):
    return math.sqrt(distSquared(a,b))

def arr_sum(first_arr, second_arr):
    output = []
    for i in range(len(first_arr)):
        output.append(first_arr[i] + second_arr[i])
    return output

class Node:
    def __init__(self, position, generation, parent, variance):
        self.pos = position
        self.gen = generation
        self.gen.append(self)
        self.child = []
        self.par = parent
        self.guide = 0
        self.var = variance
    
    def set_guiding_angle(self, theta):
        self.guide = theta
    
    def make_children(self, next):
        for _ in range(2):
            angle = random.random() * 2 * self.var - self.var + self.guide
            self.child.append(Node(arr_sum(self.pos, [math.cos(angle), math.sin(angle)]), next, self, self.var))
            
    def plot_trace_path_helper(self, arr, plot, col):
        """Plot the path of this Node.
        
        Keyword arguments:
        arr -- a record of this Node's parent's location"""
        for child in self.child:
        # For each child of this Node:
            child.plot_trace_path_helper(self.pos, plot, col)
            # Recursively call the helper function with this Node's true position array.
        # plot.plot([arr[0], self.pos[0]], [arr[1], self.pos[1]], color = (0, 0, 0, .1))
        # Plot the line between this Node and its parent.
        if self.child == []:
        # If this Node has no children:
            plot.plot([self.pos[0]], [self.pos[1]], 'o', color = col)
            # Plot the position of this Node as a dot.
    
    def plot_trace_path(self, plot, col):
        """Plot the path of this Node."""
        for child in self.child:
        # For each child of the Node:
            child.plot_trace_path_helper(self.pos, plot, col)
            # Call the helper function with this Node's true position array.

living = []
next = []
root = Node([0, 0], living, None, math.radians(15))

generation = 0
generations = 10

def f_t(t):
    # return math.exp(-t / 5)
    # return math.pow(.9, t)
    # return 1/2 * (-math.log(t + 1, math.e) + 3)
    # return 1
    # return math.log(math.log(t + 2) + 2) / (t + 2)
    # return 0.25
    # return math.sin(t) / 3 + 0.5
    return math.sinh(1 / (t + 1))

fig, (ax1, ax2) = plot.subplots(1, 2, figsize = (10, 5))
ax1.set_title("Sample random simulation")
ax2.set_title("Cluster count by generation")
# root.plot_trace_path(ax1)

clusters = []
repeats = 10

for k in range(repeats):
    col = color.hsv_to_rgb((k / repeats, 1, 1))
    # Set the color of dots.
    col = (col[0], col[1], col[2], 0.1)
    clusters.append([])
    while generation < generations:
        print("Running generation", generation + 1)
        num = len(living)
        edges = []
        f = f_t(generation)
        f *= f
        # print(f)
        for i in range(num):
            for j in range(i+1, num):
                d = distSquared(living[i].pos, living[j].pos)
                if d < f:
                    edges.append((i, j))
        g = ig.Graph(num, edges)
        components = g.connected_components(mode='weak')
        # print(clusters)
        clusters[k].append(len(components))
        coord = [-1] * num
        angles = []
        for index, component in enumerate(components):
            for node in component:
                coord[node] = index
            angles.append(random.random() * 2 * math.pi)
        for index, node in enumerate(living):
            
            node.set_guiding_angle(angles[coord[index]])
            node.make_children(next)
        # print(coord)
        # print(angles)
        living = next
        next = []
        
        generation += 1
    
    living = []
    next = []
    root.plot_trace_path(ax1, col)
    root = Node([0, 0], living, None, math.radians(15))
    generation = 0



granularity = 360
# Define the granularity of the circle (The higher, the more accurate).
for j in range(1, math.ceil(generations + 1)):
# For each value between 1 and the longest path of a Node: 
    circ_path = [[], []]
    # Initialize a path array.
    for i in range(granularity):
    # For each i in the range of granularity:
        circ_path[0].append(j * math.cos(math.radians(360 * i / granularity)))
        # Append the x coordinate of a circle with radius j at angle i * 2pi / granularity to the array.
        circ_path[1].append(j * math.sin(math.radians(360 * i / granularity)))
        # Append the y coordinate of a circle with radius j at angle i * 2pi / granularity to the array.
    circ_path[0].append(j)
    # Close the circular path by appending j to the x coordinate array.
    circ_path[1].append(0)
    # Close the circular path by appending 0 to the y coordinate array.
    if j % 5 == 0:
    # If the radius is a multiple of 5: 
        ax1.plot(circ_path[0], circ_path[1], color = (0, 0, 0, 1))
        # Plot a green circle.
    else:
    # Otherwise:
        ax1.plot(circ_path[0], circ_path[1], color = (.5, .5, .5, 1))
        # Plot a blue circle.
ax1.plot([0], [0], 'o', color = (0, 1, 0, 1))
# Plot a green dot in the center.
# print(clusters)
for i in range(repeats):
    col = color.hsv_to_rgb((i / repeats, 1, 1))
    ax2.plot(range(generations), clusters[i], color = col)

plot.show()