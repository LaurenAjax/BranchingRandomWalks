import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color
import functools as ft

def get_angles(source, target, sRad, tRad, probability, rangeArr):
    d = distBetween(source, target)
    l = (pow(sRad, 2) - pow(tRad, 2) + pow(d, 2)) / (2 * d)
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

def clamped(a, b, c):
    return (a > b) & (a < c)

def clamp(a, b, c):
    # if b > c:
    #     if a < b:
    #         return
    #     if a <= c:
    #         return 
    #     return a
    # if a < b:
    #     return b
    # if a > c:
    #     return c
    return a

def lerp(a, b, t):
    return a * (1 - t) + b * t

def lerp_arr(a, b, min, max, delta):
    output = []
    t = min
    while t <= max:
        output.append(lerp(a, b, t))
        t += delta
    return output

def distBetween(a,b):
    return math.sqrt(distSquared(a, b))

def distSquared(a,b):
    dist = 0
    for i,j in a,b:
        dist += (i - j) * (i - j)
    return dist
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

class Node:
    def __init__(self, loc, theta, gen, par, stepLen, dF, cPF, rF, pF, spr, dev, alp):
        self.position = loc
        self.bearing = (theta + math.pi) % (2 * math.pi) - math.pi
        self.generation = gen
        self.parent = par
        self.children = []
        self.stepSize = stepLen
        self.densityFunc = dF
        self.childPopFunc = cPF
        self.radius = rF
        self.probability = pF
        self.spread = spr
        self.deviation = dev
        self.alpha = alp
        
    def get_cousins(self):
        """Get a 2D array of all cousins of this Node.
        
        If you access output[i], it will be an array of ith cousins.
        
        Fun fact, siblings can be referred to as 0th cousins."""
        cousins = []
        uncommon_ancestor = self
        common_ancestor = uncommon_ancestor.parent
        degree = 0
        while common_ancestor is not None:
            cousins.append([])
            for nth_uncle in common_ancestor.children:
                if nth_uncle is not uncommon_ancestor:
                    nth_uncle.get_living(cousins[degree], degree)
            uncommon_ancestor = common_ancestor
            common_ancestor = uncommon_ancestor.parent
            degree += 1
        return cousins
    
    def get_child_cousins(self):
        """Get a 2D array of all cousins of the children of this Node.
        
        If you access output[i], it will be an array of ith cousins.
        
        Fun fact, siblings can be referred to as 0th cousins."""
        cousins = [[]]
        uncommon_ancestor = self
        common_ancestor = uncommon_ancestor.parent
        degree = 1
        while common_ancestor is not None:
            cousins.append([])
            for nth_uncle in common_ancestor.children:
                if nth_uncle is not uncommon_ancestor:
                    nth_uncle.get_living(cousins[degree], degree + 1)
            uncommon_ancestor = common_ancestor
            common_ancestor = uncommon_ancestor.parent
            degree += 1
        return cousins
                    
    def get_living(self, arr, degree):
        if degree > 0:
            for child in self.children:
                child.get_living(arr, degree - 1)
        else:
            arr.append(self)

    def propogate_me(self):
        cousins = self.get_child_cousins()
        onceRem = self.get_cousins()
        if self.generation < 1:
            for i in range(self.childPopFunc(self, self.generation, 0, onceRem)):
                angle = random.random() * math.pi * 2
                bearing = [math.cos(angle), math.sin(angle)]
                self.children.append(Node(arr_sum(bearing, self.position), angle, self.generation + 1, self, self.stepSize, self.densityFunc, self.childPopFunc, self.radius, self.probability, self.spread, self.deviation, self.alpha))
            return
        density = self.densityFunc(self, onceRem)
        spread = lerp(self.spread / 180 * math.acos(-density), self.spread, self.alpha)
        child_count = self.childPopFunc(self, self.generation, density, onceRem)
        regions = []
        for degree in range(len(cousins)):
            for cousin in cousins[degree]:
                r = self.radius(self.generation, degree, density, onceRem)
                if clamped(distBetween(self.position, cousin.position), self.stepSize - r, self.stepSize + r):
                    get_angles(self.position, cousin.position, self.stepSize, r, lerp(1, self.probability(self.generation, degree, density, cousins), self.alpha), regions)
        if self.bearing >= (math.pi - spread):
            true_region = [[-math.pi, self.bearing - 2 * math.pi + spread, 1], [self.bearing - spread, math.pi, 1]]
        elif self.bearing <= (spread - math.pi):
            true_region = [[-math.pi, self.bearing + spread, 1], [self.bearing + math.pi * 2 - spread, math.pi, 1]]
        else:
            true_region = [[self.bearing - spread, self.bearing + spread, 1]]
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
        # for true in true_region:
        #     if true[0] > true[1]:
        #         print("Uh oh")
        #         print(true)
        scale = 0
        probability = []
        for region in true_region:
            prob = (region[1] - region[0]) * region[2] / math.pi 
            # print("Prob 1:",prob)
            probability.append(prob)
            scale += prob
        # print("next")
        for prob in range(len(probability)):
            probability[prob] /= scale
            # print(probability[prob])
        i = 0
        rand = random.random()
        while  (rand > probability[i]):
            rand -= probability[i]
            i += 1
        angle = (random.random() * (true_region[i][1] - true_region[i][0])) + true_region[i][0]
        bearing = [math.cos(angle), math.sin(angle)]
        self.children.append(Node(arr_sum(bearing, self.position), angle, self.generation + 1, self, self.stepSize, self.densityFunc, self.childPopFunc, self.radius, self.probability, self.spread, self.deviation, self.alpha))
        for i in range(1, child_count):
            next_angle = angle + (random.random() * 2 - 1) * math.radians(self.deviation)
            next_angle = clamp(next_angle, self.bearing - math.pi / 2, self.bearing - math.pi / 2) # No clue how to do this right
            bearing = [math.cos(next_angle), math.sin(next_angle)]
            self.children.append(Node(arr_sum(bearing, self.position), next_angle, self.generation + 1, self, self.stepSize, self.densityFunc, self.childPopFunc, self.radius, self.probability, self.spread, self.deviation, self.alpha))

    def propogate_descendants(self, num):
        if num == 0:
            self.propogate_me()
        else:
            for child in self.children:
                child.propogate_descendants(num - 1)
    
    def run_gens(self, num, **kwargs):
        """Generate the num'th generation after this Node.
        
        Keyword arguments:
        num -- the last generation to run
        **kwargs arguments:
        last -- the last generation ran in the past"""
        last = kwargs.get('last', 0)
        # If the last generation ran in the past was specified, store it in last.
        # Otherwise, store 0 in last.
        for i in range(last, num):
        # For each i between last (incl.) and num (excl.)
            print("Running gen", i+1, "/", num)
            # Print that generation i+1 out of num is being run.
            self.propogate_descendants(i)
            # Generate that generation.
        print("Generation finished")
        # Print that generation is finished.
        
    def get_density(self, onceRem):
        """Get this Node's density."""
        return self.densityFunc(self, self.generation, onceRem)
    
    def plot_trace_path_helper(self, arr):
        """Plot the path of this Node.
        
        Keyword arguments:
        arr -- a record of this Node's parent's location"""
        for child in self.children:
        # For each child of this Node:
            child.plot_trace_path_helper(self.position)
            # Recursively call the helper function with this Node's true position array.
        plot.plot([arr[0], self.position[0]], [arr[1], self.position[1]], color=(0, 0, 0, .1))
        # Plot the line between this Node and its parent.
        if self.children == []:
        # If this Node has no children:
            plot.plot([self.position[0]], [self.position[1]], 'o', color=(1, 0, 0, .1))
            # Plot the position of this Node as a dot.
    
    def plot_trace_path(self):
        """Plot the path of this Node."""
        for child in self.children:
        # For each child of the Node:
            child.plot_trace_path_helper(self.position)
            # Call the helper function with this Node's true position array.

def dA(s, pop):
    """A defined density function.
    
    Returns the density according to the sum of 1/(1+x^2), where x is the distance to any Node in the same generation."""
    density = 0
    for degree in range(len(pop)):
        for cousin in pop[degree]:
            density += 1 / (1 + distSquared(s.position, cousin.position))
    return 1 / (1 + math.exp(.25*(10 - density)))

def dB(s, pop):
    """A defined density function.
    
    Returns the density according to the number of Nodes within 1 unit in the same generation."""
    density = 0
    for degree in range(len(pop)):    
        for cousin in pop[degree]:
            if distSquared(s.position, cousin.position) < 25:
                density += 1
    return 1 / (1 + math.exp(.25*(10 - density)))

def dC(s, pop):
    """A defined density function.
    
    Returns the density according to the number of Nodes within 1 unit in the same generation."""
    density = 0
    for degree in range(len(pop)):    
        for cousin in pop[degree]:
            if abs(s.position[0]-cousin.position[0]) + abs(s.position[1] - cousin.position[1]) < 5:
                density += 1
    return 1 / (1 + math.exp(.25*(10 - density)))

def cA(s, gen, den, pop):
    if gen < 1:
        return 10
    return 2

def cB(s, gen, den, pop):
    """A defined propogation function.
    
    Returns that a random number of chihldren are expected based on the density.
    
    Expects a density in (0,1) """
    if gen < 1:
        return 10
    return 2 + round(3 * den * random.random())

def cC(s, gen, den, pop):
    """A defined propogation function.
    
    Returns that a random number of chihldren are expected based on the density."""
    return 3

def cD(s, gen, den, pop):
    """A defined propogation function.
    
    Returns that a random number of chihldren are expected based on the density."""
    if gen < 1:
        return 10
    if den > 0.5:
        return random.randint(2, 5)
    return random.randint(0, 2)

def rA(n, k, den, pop):
    if k >= 20:
        return 0
    return pow(0.9, k)

def rB(n, k, den, pop):
    return pow(0.9, n) * k

def pA(n, k, den, pop):
    # return 0.9 - k * 0.1
    # return max(0.9 - 0.1 * k, 0.1)
    return .1


rootParams = [[0,0], 0, 0, None, 1, dC, cA, rB, pA, 90, 5]
root = Node(*rootParams, 1)
alphaArr = lerp_arr(0, 1, 0, 1, .125)
print(alphaArr)
gens = 10

# Set the number of generations to run for
# plot.figure(1, figsize=(6,6))
# Set the dimensions of the output window to 6 by 6.

# EXPERIMENTAL BELOW
# 
# plot.figure(2, figsize=(20,6))
# for i in range(gens):
#     plot.subplot(2,5,i + 1)
#     print("Running gen", i+1, "/", gens)
#     root.propogate_descendants(i)
#     root.plot_trace_path()
#     granularity = 360
#     # Define the granularity of the circle (The higher, the more accurate).
#     for j in range(1, math.ceil(gens + 1)):
#     # For each value between 1 and the longest path of a Node: 
#         circ_path = [[], []]
#         # Initialize a path array.
#         for i in range(granularity):
#         # For each i in the range of granularity:
#             circ_path[0].append(j * math.cos(math.radians(360 * i / granularity)))
#             # Append the x coordinate of a circle with radius j at angle i * 2pi / granularity to the array.
#             circ_path[1].append(j * math.sin(math.radians(360 * i / granularity)))
#             # Append the y coordinate of a circle with radius j at angle i * 2pi / granularity to the array.
#         circ_path[0].append(j)
#         # Close the circular path by appending j to the x coordinate array.
#         circ_path[1].append(0)
#         # Close the circular path by appending 0 to the y coordinate array.
#         if j % 5 == 0:
#         # If the radius is a multiple of 5: 
#             plot.plot(circ_path[0], circ_path[1], color = (0, 0, 0, 1))
#             # Plot a green circle.
#         else:
#         # Otherwise:
#             plot.plot(circ_path[0], circ_path[1], color = (.5, .5, .5, 1))
#             # Plot a blue circle.
#     plot.plot([0], [0], 'o', color = (0, 0, 0, 1))

root.run_gens(gens)

root.plot_trace_path()

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
        plot.plot(circ_path[0], circ_path[1], color = (0, 0, 0, 1))
        # Plot a green circle.
    else:
    # Otherwise:
        plot.plot(circ_path[0], circ_path[1], color = (.5, .5, .5, 1))
        # Plot a blue circle.
plot.plot([0], [0], 'o', color = (0, 1, 0, 1))
# Plot a green dot in the center.



plot.show()