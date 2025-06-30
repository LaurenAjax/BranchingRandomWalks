import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import random
import math

class Node:
    def __init__(self, parent, angle, x_coord, y_coord, num_kids, gen):
        self.parent = parent
        # the parent node
        self.angle = angle
        # the angle at which the node is from the parent node
        self.x_coord = x_coord
        # the node's position on the x-axis
        self.y_coord = y_coord
        # the node's position on the y-axis
        self.num_kids = num_kids
        # the number of kids this node will have
        self.next = []
        # a list of all this node's kids
        self.gen = gen
        # the generation this node is a part of

    def build_plot(self):
        plt.plot(self.x_coord, self.y_coord, 'o', color = (0, 0, 1, 0.1))
        # plots the ending nodes
        x_array = [self.x_coord]
        # creates a list of x-coordinates this node has traveled
        y_array = [self.y_coord]
        # creates a list of y coordinates this node has traveled
        cur_parent = self.parent
        # the current parent node
        while cur_parent is not None:
            plt.plot(cur_parent.x_coord, cur_parent.y_coord, 'o', color = (1, 0, 0, 0.1))
            # plots the parent node
            x_array.append(cur_parent.x_coord)
            # adds the parent node's x-coordinate to the array
            y_array.append(cur_parent.y_coord)
            # adds the parent node's y-coordinate to the array
            cur_parent = cur_parent.parent
            # moves the plot one generation back
        plt.plot(x_array, y_array, color = (0, 0, 0, 0.1))
        # plots the path in its entirety
    
    def removed(self, other):
        if(self.gen != other.gen):
            return None
        first_parent = self.parent
        second_parent = other.parent
        while first_parent is not second_parent:
            first_parent = first_parent.parent
            second_parent = second_parent.parent
        return self.gen - first_parent.gen - 1

    def change_node_position(self):
        self.angle = random.randint(self.parent.angle - 85, self.parent.angle + 85)
        self.x_coord = self.parent.x_coord + math.cos(math.radians(self.angle))
        self.y_coord = self.parent.y_coord + math.sin(math.radians(self.angle))

root = Node(None, 0, 0, 0, 2, 0)

def generate_node(parent_node, parent_x, parent_y, parent_gen, lower_bound, upper_bound):
    angle = random.randint(lower_bound, upper_bound)
    x = parent_x + math.cos(math.radians(angle))
    y = parent_y + math.sin(math.radians(angle))
    if parent_gen < 9:
        return Node(parent_node, angle, x, y, 2, parent_gen + 1)
    else:
        return Node(parent_node, angle, x, y, 0, parent_gen + 1)

def build_gen(cur_gen):
    if cur_gen[0].num_kids != 0:
        next_gen = []
        firstborn = []
        for parent_node in cur_gen:
            parent_angle = parent_node.angle
            parent_x = parent_node.x_coord
            parent_y = parent_node.y_coord
            parent_num_kids = parent_node.num_kids
            parent_next = parent_node.next
            parent_gen = parent_node.gen
            if parent_gen < 4:
                for i in range(parent_node.num_kids):
                    kid_node = generate_node(parent_node, parent_x, parent_y, parent_gen, 1, 360)
                    parent_next.append(kid_node)
                    next_gen.append(kid_node)
            else:
                for i in range(parent_node.num_kids):
                    if len(next_gen) == 0 and i == 0:
                        kid_node = generate_node(parent_node, parent_x, parent_y, parent_gen, parent_node.angle - 85, parent_node.angle + 85)
                        parent_next.append(kid_node)
                        next_gen.append(kid_node)
                        firstborn.append(kid_node)
                    elif i == 0:
                        kid_angle = random.randint(parent_angle - 85, parent_angle + 85)
                        kid_x = parent_x + math.cos(math.radians(kid_angle))
                        kid_y = parent_y + math.sin(math.radians(kid_angle))
                        if parent_node.gen < 9:
                            kid_node = Node(parent_node, kid_angle, kid_x, kid_y, 2, parent_gen + 1)
                        else:
                            kid_node = Node(parent_node, kid_angle, kid_x, kid_y, 0, parent_gen + 1)
                        for cousin_node in firstborn:
                            distance = math.sqrt((kid_node.x_coord - cousin_node.x_coord)**2 + (kid_node.y_coord - cousin_node.y_coord)**2)
                            if distance < 2 * 0.9**kid_node.removed(cousin_node):
                                kid_node.change_node_position()
                        loop = 0
                        while (kid_x != kid_node.x_coord or kid_y != kid_node.y_coord) and loop < 5:
                            kid_x = kid_node.x_coord
                            kid_y = kid_node.y_coord
                            for cousin_node in firstborn:
                                distance = math.sqrt((kid_node.x_coord - cousin_node.x_coord)**2 + (kid_node.y_coord - cousin_node.y_coord)**2)
                                if distance < 2 * 0.9**kid_node.removed(cousin_node):
                                    kid_node.change_node_position()
                        parent_next.append(kid_node)
                        next_gen.append(kid_node)
                        firstborn.append(kid_node)
                    else:
                        kid_node = generate_node(parent_node, parent_x, parent_y, parent_gen, parent_node.angle - 5, parent_node.angle + 5)
                        parent_next.append(kid_node)
                        next_gen.append(kid_node)
        build_gen(next_gen)
    else:
        for node in cur_gen:
            node.build_plot()

build_gen([root])
print("Model Built!")
plt.show()