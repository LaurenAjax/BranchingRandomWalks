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
        
def arr_dif(arrA, arrB):
    """Return an array of the differences in values of two arrays.

    Keyword arguments:
    arrA -- the first array, the target (length n)
    arrB -- the second array, the source (length n)
    """
    output = []
    for i in range(len(arrA)):
        output.append(arrA[i] - arrB[i])
    return output

class Node:
    """A Node class, defined with positions, a parent, children, step length, and weights on attraction.
    
    Init arguments:
    pos    --   The position of the Node, likely inherited from its parent.
                Stored in init_pos. Expected to remain the same.
    delta  --   The change in position from the parent node.
                Stored in delta_pos. Can be altered.
    par    --   The parent of the Node.
                Stored in parent. Expected to remain the same.
    len    --   The step length of the Node.
                Stored in step_len. Expected to remain the same for this implementation, but can be altered with reason.
    weight --   An array of weights to be put on the initial delta, sibling attraction, and cousion repulsion.
                Stored in weights. Expected to remain the same for this implementation, but can be altered with reason.
                Repusion is marked with a negative.
    
    Other fields:
    true_pos -- The true position of a Node. If the position of a Node is relevant, this field should be used.
    children -- The children of a Node as an array. Expected to be filled to generate a generation."""
    true_pos = [0, 0]
    init_pos = [0, 0]
    delta_pos = [0, 0]
    parent = None
    children = []
    step_len = 1
    weights = [1, 1, 1]
    
    def __init__(self, pos, delta, par, len, weight):
        """Initialize a Node based on parameters as discussed above.
        
        Init arguments:
        pos    --   The position of the Node, likely inherited from its parent.
                    Stored in init_pos. Expected to remain the same.
        delta  --   The change in position from the parent node.
                    Stored in delta_pos. Can be altered.
        par    --   The parent of the Node.
                    Stored in parent. Expected to remain the same.
        len    --   The step length of the Node.
                    Stored in step_len. Expected to remain the same for this implementation, but can be altered with reason.
        weight --   An array of weights to be put on the initial delta, sibling attraction, and cousion repulsion.
                    Stored in weights. Expected to remain the same for this implementation, but can be altered with reason.
                    Repusion is marked with a negative."""
        self.init_pos = pos
        self.delta_pos = delta
        self.step_len = len
        self.true_pos = [0, 0]

        self.calcTruePos()
        # Generate the value of true_pos from the given delta and init_pos.
        self.parent = par
        self.weights = weight
        self.children = []
        # Initialize an empty array for children.
        
    def calcTruePos(self):
        """Calculate the true position of the Node based on init_pos and delta_pos."""
        scale_factor = random.randint(1,3) / 2
        # Generate a scale factor for the step length
        for i in range(2):
        # For each index in the position arrays:
            self.true_pos[i] = self.init_pos[i] + self.delta_pos[i] * self.step_len * scale_factor
            # Set the true_pos' ith value to the init_pos' ith value plus the delta_pos' ith value scaled
    
    def relation_movement(self):
        """Calculate the informed delta_pos array based on sibling and cousin locations."""
        cousin_arr = []
        sibling_arr = []
        # Initialize empty cousin and sibling arrays
        if self.parent is not None:
        # If this Node has a parent:
            grand_par = self.parent.parent
            # Store this Node's grandparent (May be None)
            if grand_par is not None:
            # If this Node has a grandparent (Not None):
                for uncle in grand_par.children:
                # For each child of the grand parent:
                    if uncle is self.parent:
                    # Check if the child is the parent of this Node, and if it is:
                        for sibling in uncle.children:
                        # For each sibling of the Node:
                            if sibling is not self:
                            # That isn't the node itself:
                                sibling_arr.append(sibling)
                                # Append a reference to that sibling to the sibling array
                    else:
                    # Otherwise, if the child of the grand parent is not the parent:
                        for cousin in uncle.children:
                        # For each cousin of the Node:
                            cousin_arr.append(cousin)
                            # Append a reference to that cousin to the cousin array
            else:
            # Otherwise, this Node has no grandparent:
                for sibling in self.parent.children:
                # For each sibling of the Node:
                    if sibling is not self:
                    # That isn't the node itself:
                        sibling_arr.append(sibling)
                        # Append a reference to that sibling to the sibling array
            sibling_pull = ft.reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], map(lambda x: scale_arr(arr_dif(x.true_pos, self.true_pos), pow(self.inv_dist_to(x.true_pos), 3)), sibling_arr), [0, 0])
            # For each sibling in the sibling array, calculate the array between this Node's true position and the sibling's.
            # Then, scale that array by the inverse of the distance between the Node's true positions, taken to some power.
            # Then, finally, sum all of the arrays together.
            cousin_push = ft.reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], map(lambda x: scale_arr(arr_dif(x.true_pos, self.true_pos), pow(self.inv_dist_to(x.true_pos), 3)), cousin_arr), [0, 0])
            # For each cousin in the cousin array, calculate the array between this Node's true position and the cousin's.
            # Then, scale that array by the inverse of the distance between the Node's true positions, taken to some power.
            # Then, finally, sum all of the arrays together.
            sibling_pull = to_unit(sibling_pull)
            # Convert the sibling array to a unit array.
            cousin_push = to_unit(cousin_push)
            # Convert the cousin array to a unit array.
            for i in range(2):
            # For each index of delta_pos:
                self.delta_pos[i] = self.delta_pos[i] * self.weights[0] + sibling_pull[i] * self.weights[1] + cousin_push[i] * self.weights[2]
                # Set the ith value to the sum of the delta_pos, sibling array, and cousin array's ith values scaled by the weights array.
            self.delta_pos = to_unit(self.delta_pos)
            # Convert the delta_pos array to a unit array.

    def inv_dist_to(self, arr):
        """Return the inverted distance between this Node and a position array.

        Keyword arguments:
        arr -- the array of numbers (len = 2)
        """
        result = self.dist_to(arr)
        # Calculate the normal distance between this Node and a position array.
        if result == 0:
        # If the distance is zero:
            return 0
            # Return 0.
        return 1 / result
        # Otherwise, return 1 divided by the distance
    
    def dist_to(self, arr):
        """Return the distance between this Node and a position array.

        Keyword arguments:
        arr -- the array of numbers (len = 2)
        """
        return math.sqrt(math.pow(arr[0] - self.true_pos[0], 2) + math.pow(arr[1] - self.true_pos[1], 2))
        # Calculate and return the distance between this Node and a position array.
    
    def new_gen(self):
        """Generate children for this Node."""
        if self.dist_to([0, 0]) < 5:
        # If the distance to the origin is less than 5 units:
            count = random.randint(1, 6)
            # Generate a random number of kids between 1 and a number.
        else:
        # Otherwise:
            count = 2
            # Generate two kids.
        for i in range(count):
        # For the specified number of kids:
            dir = math.radians(random.randint(1, 360))
            # Generate a random direction uniformly.
            self.children.append(Node(self.true_pos, [math.cos(dir),math.sin(dir)], self, self.step_len, self.weights))
            # Create and append a new Node with:
            #   This Node's true_pos as its init_pos.
            #   An initial delta_pos array pointing in the random direction with unit magnitude.
            #   This Node as its parent.
            #   This Node's step length as its own.
            #   This Node's weights as its own.
            # to this Node's children.
    
    def propogate(self, num):
        """Generate the num'th generation after this Node.
        
        Keyword arguments:
        num -- the generation's past this node"""
        if num == 0:
        # If the num is 0:
            self.new_gen()
            # Generate a new generation of this Node.
        elif num == 1:
        # Otherwise, if its 0:
            for child in self.children:
            # For each child of this Node:
                child.new_gen()
                # Generate a new generation of that child Node.
            for child in self.children:
            # Then, for each child of this Node:
                for grandchild in child.children:
                # For each grandchild to this Node:
                    grandchild.relation_movement()
                    # Calculate their informed delta_pos arrays based on sibling and cousin locations.
            # Then, for each child of this Node:
                for grandchild in child.children:
                # For each grandchild to this Node:
                    grandchild.calcTruePos()
                    # Calculate their true positions based on their init_pos and newly informed delta_pos.
        else:
        # Otherwise:
            for child in self.children:
            # For each child of this Node:
                child.propogate(num - 1)
                # Call this function with one lesser num.
    
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
            self.propogate(i)
            # Generate that generation.
        print("Generation finished")
        # Print that generation is finished.
            
    def plot_path_helper(self, arr):
        """Plot the path of this Node.
        
        Keyword arguments:
        arr -- a record of this Node's ancestor's locations, mutable"""
        arr[0].append(self.true_pos[0])
        # Append this Node's position's x coordinate to the array.
        arr[1].append(self.true_pos[1])
        # Append this Node's position's y coordinate to the array.
        for child in self.children:
        # For each child of this Node:
            child.plot_path_helper(arr)
            # Recursive call this function with the new array.
        if self.children == []:
        # If this Node has no children:
            plot.plot(arr[0], arr[1], color=(0, 0, 0, .1))
            # Plot the path of the array.
            plot.plot([arr[0].pop()], [arr[1].pop()], 'o', color=(1, 0, 0, .1))
            # Plot the final position as a dot.
            # Additionally, remove this Node's position from the array.
        else:
        # Otherwise:
            arr[0].pop()
            # Remove this Node's x position from the array.
            arr[1].pop()
            # Remove this Node's y position from the array.
            
    def plot_path(self):
        """Plot the path of this Node."""
        self.plot_path_helper([[], []])
        # Call the helper function with an empty position array.
        
    def plot_singular_path_helper(self, arr):
        """Plot the path of this Node.
        
        Keyword arguments:
        arr -- a record of this Node's parent's location"""
        for child in self.children:
        # For each child of this Node:
            child.plot_singular_path_helper(self.true_pos)
            # Recursively call the helper function with this Node's true position array.
        plot.plot([arr[0], self.true_pos[0]], [arr[1], self.true_pos[1]], color=(0, 0, 0, .1))
        # Plot the line between this Node and its parent.
        if self.children == []:
        # If this Node has no children:
            plot.plot([self.true_pos[0]], [self.true_pos[1]], 'o', color=(1, 0, 0, .1))
            # Plot the position of this Node as a dot.
    
    def plot_singular_path(self):
        """Plot the path of this Node."""
        for child in self.children:
        # For each child of the Node:
            child.plot_singular_path_helper(self.true_pos)
            # Call the helper function with this Node's true position array.


step_length = 3
# Define the step length the Node's will have (integer expected).
root = Node([0, 0], [0, 0], None, step_length, [1, .5, -2])
# Initialize the root Node. Parameters of the simulation are best modified on this line.
gens = 10
# Set the number of generations to run for.
root.run_gens(gens)
# Run that many generations.
plot.axis([-gens * step_length, gens * step_length, -gens * step_length, gens * step_length])
# Generate the axes of the plot based on the number of generations and the step length,
plot.grid(True)
# Enable the plot's grid.
ticks = []
# Initialize the ticks array to be empty.
for i in range(2 * step_length + 1):
# For 2 * step_length + 1:
    ticks.append(gens * i * 1.5 - gens * step_length * 1.5)
    # Generate a tick line uniformly along the range of values.
plot.xticks(ticks)
# Plot the x ticks.
plot.yticks(ticks)
# Plot the y ticks.
root.plot_singular_path()
# Plot the path of the root Node.
granularity = 360
# Define the granularity of the circle (The higher, the more accurate)
for j in range(1, math.ceil(gens * step_length * 1.5 + 1)):
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