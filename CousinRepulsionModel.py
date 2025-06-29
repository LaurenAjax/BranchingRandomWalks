import matplotlib.pyplot as plt
import random
import math

class Node:
    def __init__(self, parent, angle, x_coord, y_coord, num_kids, gen):
        self.parent = parent
        self.angle = angle
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.num_kids = num_kids
        self.next = []
        self.gen = gen

root = Node(None, 0, 0, 0, 2, 0)

def removed(first_node, second_node):
    if(first_node.gen != second_node.gen):
        return None
    first_parent = first_node.parent
    second_parent = second_node.parent
    while first_parent is not second_parent:
        first_parent = first_parent.parent
        second_parent = second_parent.parent
    return first_node.gen - first_parent.gen - 1

def generate_node(parent_node, lower_bound, upper_bound):
    angle = random.randint(lower_bound, upper_bound)
    kid_x = parent_node.x_coord + math.cos(angle)
    kid_y = parent_node.y_coord + math.sin(angle)
    if parent_node.gen < 29:
        return Node(parent_node, angle, kid_x, kid_y, 2, parent_node.gen + 1)
    else:
        return Node(parent_node, angle, kid_x, kid_y, 0, parent_node.gen + 1)

def change_node_position(node):
    node.angle = random.randint(node.parent.angle - 85, node.parent.angle + 85)
    node.x_coord = node.parent.x_coord + math.cos(node.angle)
    node.y_coord = node.parent.y_coord + math.sin(node.angle)

def build_gen(cur_gen):
    next_gen = []
    for parent_node in cur_gen:
        if parent_node.gen < 10:
            for i in range(parent_node.num_kids):
                kid_node = generate_node(parent_node, 1, 360)
                parent_node.next.append(kid_node)
                next_gen.append(kid_node)
        else:
            firstborn = []
            for i in range(parent_node.num_kids):
                if len(next_gen) == 0 and i == 0:
                    kid_node = generate_node(parent_node, parent_node.angle - 85, parent_node.angle + 85)
                    parent_node.next.append(kid_node)
                    next_gen.append(kid_node)
                    firstborn.append(kid_node)
                elif i == 0:
                    angle = random.randint(parent_node.angle - 85, parent_node.angle + 85)
                    kid_x = parent_node.x_coord + math.cos(angle)
                    kid_y = parent_node.y_coord + math.sin(angle)
                    if parent_node.gen < 29:
                        kid_node = Node(parent_node, angle, kid_x, kid_y, 2, parent_node.gen + 1)
                    else:
                        kid_node = Node(parent_node, angle, kid_x, kid_y, 0, parent_node.gen + 1)
                    for cousin_node in firstborn:
                        distance = math.sqrt((kid_node.x_coord - cousin_node.x_coord)**2 + (kid_node.y_coord - cousin_node.y_coord)**2)
                        if distance < 0.9**removed(kid_node, cousin):
                            change_node_position(kid_node)
                    loop = 0
                    while (kid_x != kid_node.x_coord or kid_y != kid_node.y_coord) and loop < 5:
                        kid_x = kid_node.x_coord
                        kid_y = kid_node.y_coord
                        for cousin_node in firstborn:
                            distance = math.sqrt((kid_node.x_coord - cousin_node.x_coord)**2 + (kid_node.y_coord - cousin_node.y_coord)**2)
                            if distance < 0.9**removed(kid_node, cousin):
                                change_node_position(kid_node)
                    parent_node.next.append(kid_node)
                    next_gen.append(kid_node)
                    firstborn.append(kid_node)
                else:
                    kid_node = generate_node(parent_node, parent_node.next[0].angle - 5, parent_node.next[0].angle + 5)
                    parent_node.next.append(kid_node)
                    next_gen.append(kid_node)
    build_gen(next_gen)

build_gen([root])