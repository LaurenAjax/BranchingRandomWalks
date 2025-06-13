import random
import copy
import matplotlib.pyplot as plot
import math

class Node:
    def __init__(self, parent, theta_coord, r_coord, num_kids, gen):
        self.theta_coord = theta_coord
        self.r_coord = r_coord
        self.parent = None
        self.num_kids = num_kids
        self.next = []
        self.gen = gen


theta = 0
r = 0
root = Node(None, theta, r, random.randint(0, 5), 0)
lst = [root]
count = 0

while count < len(lst):
    for i in range(lst[count].num_kids):
        random_value = random.randint(1, 22)
        if random_value < 8:
            random_degree = random.randint(-10, 10)
        elif random_value < 15:
            random_degree = random.randint(110, 130)
        elif random_value < 22:
            random_degree = random.randint(230, 250)
        else:
            random_degree = random.randint(1, 360)
        cur_gen = lst[count].gen + 1
        if cur_gen == 10:
            cur_node = Node(lst[count], random_degree, lst[count].r_coord + 1, 0, cur_gen)
        else:
            cur_node = Node(lst[count], random_degree, lst[count].r_coord + 1, random.randint(0, 5), cur_gen)
        lst[count].next.append(cur_node)
        lst.append(cur_node)
    count += 1

for node in lst:
    plot.polar(math.radians(node.theta_coord), node.r_coord, 'o', color=(0, 0, 0, 0.3))

plot.show()