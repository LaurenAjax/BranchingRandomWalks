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
            # verifies that this node and other are of the same generation
        first_parent = self.parent
        # this node's parent node
        second_parent = other.parent
        # other's parent node
        while first_parent is not second_parent:
            # retraces to the point where this node and other share a parent
            first_parent = first_parent.parent
            second_parent = second_parent.parent
        return self.gen - first_parent.gen - 1
        # returns how far removed this node and other are from each other

    def change_node_position(self):
        self.angle = random.randint(self.parent.angle - 85, self.parent.angle + 85)
        # sets this nodes angle to a new random value
        self.x_coord = self.parent.x_coord + math.cos(math.radians(self.angle))
        # changes this node's x-coordinate based on the new angle
        self.y_coord = self.parent.y_coord + math.sin(math.radians(self.angle))
        # changes this node's y-coordinate based on the new angle

root = Node(None, 0, 0, 0, 2, 0)

def generate_node(parent_node, parent_x, parent_y, parent_gen, lower_bound, upper_bound):
    angle = random.randint(lower_bound, upper_bound)
    # gets an angle within the given bounds
    x = parent_x + math.cos(math.radians(angle))
    # determines the x-coordinate of a point at the angle from the parent and distance 1
    y = parent_y + math.sin(math.radians(angle))
    # determines the y-coordinate of a point at the angle from the parent and distance 1
    if parent_gen < 9:
        return Node(parent_node, angle, x, y, 2, parent_gen + 1)
        # returns a node that will have two kids
    else:
        return Node(parent_node, angle, x, y, 0, parent_gen + 1)
        # returns a node that will have zero kids, terminating the tree

def build_gen(cur_gen):
    if cur_gen[0].num_kids != 0:
        next_gen = []
        # all kids in the next generation
        firstborn = []
        # the firstborn kid of each parent in this generation
        for parent_node in cur_gen:
            parent_angle = parent_node.angle
            # the parent's angle
            parent_x = parent_node.x_coord
            # the parent's x-coordinate
            parent_y = parent_node.y_coord
            # the parent's y-coordinate
            parent_num_kids = parent_node.num_kids
            # the parent's number of kids
            parent_next = parent_node.next
            # a list of all the parent's kids
            parent_gen = parent_node.gen
            # the parent's generation
            if parent_gen < 4:
                for i in range(parent_node.num_kids):
                    kid_node = generate_node(parent_node, parent_x, parent_y, parent_gen, 1, 360)
                    # generates a node with a random angle
                    parent_next.append(kid_node)
                    # adds the node to its parent's list of kids
                    next_gen.append(kid_node)
                    # adds the node to the list of kids in this generation
            else:
                for i in range(parent_node.num_kids):
                    if len(next_gen) == 0 and i == 0:
                        kid_node = generate_node(parent_node, parent_x, parent_y, parent_gen, parent_node.angle - 85, parent_node.angle + 85)
                        # generates a node with an angle within 170 degrees of the parent's angle
                        parent_next.append(kid_node)
                        # adds the node to its parent's list of kids
                        next_gen.append(kid_node)
                        # adds the node to the list of kids in this generation
                        firstborn.append(kid_node)
                    elif i == 0:
                        kid_angle = random.randint(parent_angle - 85, parent_angle + 85)
                        # generates an angle within 170 degrees of the parent's angle
                        kid_x = parent_x + math.cos(math.radians(kid_angle))
                        # determines the x-coordinate of a point at the angle from the parent and distance 1
                        kid_y = parent_y + math.sin(math.radians(kid_angle))
                        # determines the y-coordinate of a point at the angle from the parent and distance 1
                        if parent_node.gen < 9:
                            kid_node = Node(parent_node, kid_angle, kid_x, kid_y, 2, parent_gen + 1)
                            # generates a node that will have two kids
                        else:
                            kid_node = Node(parent_node, kid_angle, kid_x, kid_y, 0, parent_gen + 1)
                            # generates a node that will have zero kids, terminating the tree
                        for cousin_node in firstborn:
                            distance = math.sqrt((kid_node.x_coord - cousin_node.x_coord)**2 + (kid_node.y_coord - cousin_node.y_coord)**2)
                            # calculates the distance between the cousin and the node
                            if distance < 2 * 0.9**kid_node.removed(cousin_node):
                                kid_node.change_node_position()
                                # changes the position of the node to hopefully distance it from the cousin
                        loop = 0
                        # runs the check five times
                        while (kid_x != kid_node.x_coord or kid_y != kid_node.y_coord) and loop < 5:
                            kid_x = kid_node.x_coord
                            # resets what the original x-coordinate of the node is
                            kid_y = kid_node.y_coord
                            # resets what the original y-coordinate of the node is
                            for cousin_node in firstborn:
                                distance = math.sqrt((kid_node.x_coord - cousin_node.x_coord)**2 + (kid_node.y_coord - cousin_node.y_coord)**2)
                                # calculates the distance between the cousin and the node
                                if distance < 2 * 0.9**kid_node.removed(cousin_node):
                                    kid_node.change_node_position()
                                    # changes the position of the node to hopefully distance it from the cousin
                        parent_next.append(kid_node)
                        # adds the node to its parent's list of kids
                        next_gen.append(kid_node)
                        # adds the node to the list of kids in this generation
                        firstborn.append(kid_node)
                    else:
                        kid_node = generate_node(parent_node, parent_x, parent_y, parent_gen, parent_next[0].angle - 5, parent_next[0].angle + 5)
                        # generates an angle within 10 degrees of the eldest sibling's angle
                        parent_next.append(kid_node)
                        # adds the node to its parent's list of kids
                        next_gen.append(kid_node)
                        # adds the node to the list of kids in this generation
        build_gen(next_gen)
        # starts the process again for the next generation
    else:
        for node in cur_gen:
            node.build_plot()
            # plots the path the node took to get to the end of the tree

build_gen([root])
# builds and plots the tree
plt.show()
# displays the plot