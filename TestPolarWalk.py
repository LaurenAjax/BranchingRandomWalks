import random
import copy
import matplotlib.pyplot as plot
import math

class Node:
    def __init__(self, parent, theta_coord, r_coord, num_kids, gen):
        self.parent = parent
        self.theta_coord = theta_coord
        self.r_coord = r_coord
        self.num_kids = num_kids
        self.next = []
        self.gen = gen

root = Node(None, 0, 0, random.randint(0, 10), 0)
lst = [root]
count = 0

while count < len(lst):
    cur_gen = lst[count].gen + 1
    prev_r = lst[count].r_coord
    prev_theta = lst[count].theta_coord
    prev_x = prev_r * math.cos(prev_theta)
    prev_y = prev_r * math.sin(prev_theta)
    for i in range(lst[count].num_kids):
        random_value = random.randint(1, 22)
        if random_value < 8:
            angle = math.radians(random.randint(-10, 10))
        elif random_value < 15:
            angle = math.radians(random.randint(110, 130))
        elif random_value < 22:
            angle = math.radians(random.randint(230, 250))
        else:
            angle = math.radians(random.randint(1, 360))
        cur_x = prev_x + math.cos(angle)
        cur_y = prev_y + math.sin(angle)
        cur_r = math.sqrt(cur_x**2 + cur_y**2)
        cur_theta = math.atan2(cur_y, cur_x)
        if cur_gen == 10:
            cur_node = Node(lst[count], cur_theta, cur_r, 0, cur_gen)
        else:
            cur_node = Node(lst[count], cur_theta, cur_r, random.randint(0, 4), cur_gen)
        lst[count].next.append(cur_node)
        lst.append(cur_node)
    count += 1

for node in lst:
    plot.polar(node.theta_coord, node.r_coord, 'o', color=(0, 0, 0, 0.1))
    for kid in node.next:
        plot.polar([node.theta_coord, kid.theta_coord], [node.r_coord, kid.r_coord], color=(random.random(), random.random(), random.random(), 0.5))

plot.show()