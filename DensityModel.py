import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color
import functools as ft

def to_unit(arr):
    """Return a unit vector array of an array of numbers.
    
    Sum of return array[i]^2 ~ 1.

    Keyword arguments:
    arr -- the array of numbers (any length)
    """
    scale = 0
    output = []
    for i in arr:
        scale += i*i
    scale = math.sqrt(scale)
    if scale > 0.001:
        for j in range(len(arr)):
            output.append(arr[j] / scale)
    else:
        for j in range(len(arr)):
            output.append(0)
    return output

def scale_arr(arr, scale):
    """Return a scaled array of an array of numbers.

    Keyword arguments:
    arr -- the array of numbers (any length)
    scale -- the scale factor (number expected)
    """
    output = []
    for i in range(len(arr)):
        output.append(arr[i] * scale)
    return output

def arr_sum(arrA, arrB):
    """Return an array of the sum in values of two arrays.

    Keyword arguments:
    arrA -- the first array, the target (length n)
    arrB -- the second array, the source (length n)
    """
    output = []
    for i in range(len(arrA)):
        output.append(arrA[i] + arrB[i])
    return output

def arr_dist(arrA, arrB):
    scale = 0
    for i in range(len(arrA)):
        scale += pow(arrA[i]-arrB[i],2)
    scale = math.sqrt(scale)
    return scale

class Node:
    def __init__(self, loc, bearing, pf, df, pop, gen):
        self.pos = loc
        self.dir = bearing
        self.propogation_func = pf
        # A function based on the generation number and the density of the prior generation.
        self.density_func = df
        # A function based on the generation number and the position of all elements of the prior generation.
        self.population = pop
        # A reference to Nodes of the same generation.
        self.population.append(self)
        # Add this node to its generation.
        self.generation = gen
        # The generation number.
    
    def get_density(self):
        return self.density_func(self, self.generation, self.population)        
    
    def make_children(self, next_gen_ref):
        relative_density = self.get_density()
        child_count = self.propogation_func(self, self.generation, relative_density)
        for i in range(child_count):
            bearing = random.random() * math.pi * 2
            bearing = to_unit(arr_sum([math.cos(bearing),math.sin(bearing)],scale_arr(self.dir, relative_density)))
            Node(arr_sum(bearing, self.pos), bearing, self.propogation_func, self.density_func, next_gen_ref, self.generation + 1)

def pA(s, gen, density):
    return 2

def pB(s, gen, density):
    if density >= 5:
        return random.randint(1, 2)
    return random.randint(1, math.ceil(10 / density))

def dA(s, gen, pop_arr):
    density = 0
    for i in pop_arr:
        density += 1 / (1 + pow(arr_dist(s.pos, i.pos),2))
    return density

def dB(s, gen, pop_arr):
    density = 0
    for i in pop_arr:
        if arr_dist(s.pos, i.pos) < 1:
            density += 1
    return density

living_gen = [Node([0,0], [0,0], pA, dA, [], 0)]
# Define the structure of the Node, with initial location, bearing, propogation function, density function, array of those within this generation, and the initial generation number

gens = 10
# Set the number of generations to run for

for i in range(gens):
    print("Computing gen",i+1)
    new_gen = []
    # Create an array to store the next generation.
    for parent in living_gen:
    # For each existing, living Node:
        parent.make_children(new_gen)
        # Create new children and append them to the new generation.
    living_gen = new_gen
    # Set the living_gen to the new generation.
    col = color.hsv_to_rgb((i / gens, 1, 1))
    # Set the color of dots.
    col = (col[0], col[1], col[2], math.pow(0.5,(i)/2+1))
    for node in living_gen:
    # For each living Node:
        plot.plot([node.pos[0]], [node.pos[1]], 'o', color = col)
        # Plot it.

print("Finished generation generation.")

granularity = 360
# Define the granularity of the circle (The higher, the more accurate).
for j in range(1, math.ceil(gens + 1)):
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
        plot.plot(circ_path[0], circ_path[1], color = (0, 1, 0, .1))
        # Plot a green circle.
    else:
    # Otherwise:
        plot.plot(circ_path[0], circ_path[1], color = (0, 0, 1, .1))
        # Plot a blue circle.
plot.plot([0], [0], 'o', color = (0, 1, 0, 1))
# Plot a green dot in the center.

plot.show()
# Show the plot generated by this program.