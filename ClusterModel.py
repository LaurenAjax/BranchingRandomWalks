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
        self.guide = None

    def build_plot(self):
        plt.plot(self.x_coord, self.y_coord, 'o', color = (0, 0, 1, 0.1))
        x_array = [self.x_coord]
        y_array = [self.y_coord]
        cur_parent = self.parent
        while cur_parent is not None:
            x_array.append(cur_parent.x_coord)
            y_array.append(cur_parent.y_coord)
            cur_parent = cur_parent.parent
        plt.plot(x_array, y_array, color = (0, 0, 0, 0.01))

    def build_dots(self):
        plt.plot(self.x_coord, self.y_coord, 'o', color = (1, 0, 0, 0.1))

root = Node(None, 0, 0, 0, 2, 0)

def f(t):
    return 0.9**(t + 2)

def generate_node(parent_node, num_kids, angle, gen):
    x = parent_node.x_coord + math.cos(math.radians(angle))
    y = parent_node.y_coord + math.sin(math.radians(angle))
    if parent_node.gen <= 15:
        return Node(parent_node, angle, x, y, num_kids, gen)
    else:
        return Node(parent_node, angle, x, y, 0, gen)

def build_gen(cur_gen):
    new_gen = cur_gen[0].gen + 1
    if new_gen <= 15:
        next_gen = []
        for parent_node in cur_gen:
            if parent_node.guide == None and new_gen <= 5:
                parent_node.guide = random.randint(1, 360)
            elif parent_node.guide == None:
                parent_node.guide = random.randint(parent_node.angle - 90, parent_node.angle + 90)
            for cousin_node in cur_gen:
                if cousin_node.guide == None:
                    dx = parent_node.x_coord - cousin_node.x_coord
                    dy = parent_node.y_coord - cousin_node.y_coord
                    if dx * dx + dy * dy <= f(new_gen):
                        cousin_node.guide = parent_node.guide
            for i in range(parent_node.num_kids):
                kid_node = generate_node(parent_node, 2, random.randint(parent_node.guide - 30, parent_node.guide + 30), new_gen)
                parent_node.next.append(kid_node)
                next_gen.append(kid_node)
        print("Gen " + str(new_gen) + " Built!")
        build_gen(next_gen)
    else:
        for node in cur_gen:
            node.build_plot()
            # node.build_dots()

build_gen([root])

plt.show()