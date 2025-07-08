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

    def build_plot(self):
        plt.plot(self.x_coord, self.y_coord, 'o', color = (0, 0, 1, 0.1))
        x_array = [self.x_coord]
        y_array = [self.y_coord]
        cur_parent = self.parent
        while cur_parent is not None:
            x_array.append(cur_parent.x_coord)
            y_array.append(cur_parent.y_coord)
            cur_parent = cur_parent.parent
        plt.plot(x_array, y_array, color = (0, 0, 0, 0.1))

    def removed(self, other):
        if(self.gen != other.gen):
            return None
        first_parent = self.parent
        second_parent = other.parent
        while first_parent is not second_parent:
            first_parent = first_parent.parent
            second_parent = second_parent.parent
        distance = self.gen - first_parent.gen - 1
        if distance >= 10:
            return 10
        else:
            return distance

    def density(self, x_coord_list, y_coordlist, beta):
        total = 0
        count = 0
        for x, y in zip(x_coord_list, y_coord_list):
            distance = math.sqrt((self.x_coord - x)**2 + (self.y_coord - y)**2)
            if distance < beta:
                count += 1
            if distance < 2 * beta:
                total += 1
        if total == 0:
            return 0
        else:
            return count / total
    
    def change_node_position(self, new_angle):
        self.angle = new_angle
        self.x_coord = self.parent.x_coord + math.cos(math.radians(self.angle))
        self.y_coord = self.parent.y_coord + math.sin(math.radians(self.angle))

    def change_num_kids(self, count):
        self.num_kids = count

root = Node(None, 0, 0, 0, 2, 0)
x_coord_list = [0]
y_coord_list = [0]
alpha = 0.5
beta = 1 - alpha

def build_dot_plot():
    plt.plot(x_coord_list, y_coord_list, 'o', color = (0, 0, 1, 0.1))

def generate_node(parent_node, parent_x, parent_y, parent_gen, lower_bound, upper_bound):
    angle = random.randint(lower_bound, upper_bound)
    x = parent_x + math.cos(math.radians(angle))
    y = parent_y + math.sin(math.radians(angle))
    if parent_gen < 9:
        return Node(parent_node, angle, x, y, 2, parent_gen + 1)
    else:
        return Node(parent_node, angle, x, y, 0, parent_gen + 1)

def build_gen(cur_gen):
    if cur_gen[0].gen != 10:
        next_gen = []
        firstborn = []
        for parent_node in cur_gen:
            parent_angle = parent_node.angle
            parent_x = parent_node.x_coord
            parent_y = parent_node.y_coord
            parent_num_kids = parent_node.num_kids
            parent_next = parent_node.next
            parent_gen = parent_node.gen
            upper_bound = parent_angle + 90
            lower_bound = parent_angle - 90
            upper_bound_x = parent_x + math.cos(math.radians(upper_bound))
            upper_bound_y = parent_y + math.cos(math.radians(upper_bound))
            lower_bound_x = parent_x + math.cos(math.radians(lower_bound))
            lower_bound_y = parent_y + math.cos(math.radians(lower_bound))
            if parent_gen < 4:
                for i in range(parent_node.num_kids):
                    kid_node = generate_node(parent_node, parent_x, parent_y, parent_gen, 1, 360)
                    x_coord_list.append(kid_node.x_coord)
                    y_coord_list.append(kid_node.y_coord)
                    parent_next.append(kid_node)
                    next_gen.append(kid_node)
            else:
                for i in range(parent_num_kids):
                    cousin_angles = []
                    kid_node = generate_node(parent_node, parent_x, parent_y, parent_gen, lower_bound, upper_bound)
                    for cousin_node in firstborn:
                        repelled = (10 - kid_node.removed(cousin_node))
                        if math.sqrt((cousin_node.x_coord - kid_node.x_coord)**2 + (cousin_node.y_coord - kid_node.y_coord)**2) < repelled * alpha:
                            if math.sqrt((cousin_node.x_coord - upper_bound_x)**2 + (cousin_node.y_coord - upper_bound_y)**2) > math.sqrt((cousin_node.x_coord - lower_bound_x)**2 + (cousin_node.y_coord - lower_bound_y)**2):
                                if upper_bound > kid_node.angle + repelled * 2:
                                    cousin_angles.append(kid_node.angle + repelled * 2)
                                else:
                                    cousin_angles.append(upper_bound)
                            else: 
                                if lower_bound < kid_node.angle - repelled * 2:
                                    cousin_angles.append(kid_node.angle - repelled * 2)
                                else:
                                    cousin_angles.append(lower_bound)
                    if len(cousin_angles) != 0:
                        cousin_angle = sum(cousin_angles) / len(cousin_angles)
                    else:
                        cousin_angle = kid_node.angle
                    repelled = 5 * int(4 * kid_node.density(x_coord_list, y_coord_list, beta))
                    if upper_bound - kid_node.angle > kid_node.angle - lower_bound:
                        if upper_bound > kid_node.angle + repelled:
                            density_angle = kid_node.angle + repelled
                        else: 
                            density_angle = upper_bound
                    else:
                        if lower_bound < kid_node.angle - repelled:
                            density_angle = kid_node.angle - repelled
                        else: 
                            density_angle = lower_bound
                    if kid_node.num_kids != 0:
                        kid_node.change_num_kids(2 + int(4 * kid_node.density(x_coord_list, y_coord_list, beta)))
                    kid_node.change_node_position(int((cousin_angle * alpha + density_angle * beta)))
                    x_coord_list.append(kid_node.x_coord)
                    y_coord_list.append(kid_node.y_coord)
                    parent_next.append(kid_node)
                    next_gen.append(kid_node)
                    if i == 0:
                        firstborn.append(kid_node)
        print("Gen " + str(next_gen[0].gen) + " Built!")
        build_gen(next_gen)
    else:
        for node in cur_gen:
            node.build_plot()

build_gen([root])

plt.show()