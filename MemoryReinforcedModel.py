import matplotlib.pyplot as plt
import random
import math

class Node:
    def __init__(self, parent, theta_coord, r_coord, num_kids, steps, gen):
        self.parent = parent
        self.theta_coord = theta_coord
        self.r_coord = r_coord
        self.num_kids = num_kids
        self.next = []
        self.steps = steps
        self.gen = gen

root = Node(None, 0, 0, random.randint(1, 10), random.randint(1, 5), 0)
lst = [root]
count = 0

while count < len(lst):
    cur_gen = lst[count].gen + 1
    prev_r = lst[count].r_coord
    prev_theta = lst[count].theta_coord
    prev_x = prev_r * math.cos(prev_theta)
    prev_y = prev_r * math.sin(prev_theta)
    for i in range(lst[count].num_kids):
        if (i == 0 and lst[count].parent == None):
            angle = math.radians(random.randint(1, 360))
        elif (i == 0):
            for j in range(lst[count].parent.num_kids):
                if lst[count].parent.next[j] is lst[count]:
                    angle = math.radians(random.randint(int(360 / lst[count].parent.num_kids) * j - 10, int(360 / lst[count].parent.num_kids) * j + 10))
        else:
            angle = math.radians(random.randint(int(math.degrees(lst[count].next[0].theta_coord)) - 10, int(math.degrees(lst[count].next[0].theta_coord)) + 10))
        num_steps = random.randint(1, 5)
        cur_x = prev_x + num_steps * math.cos(angle)
        cur_y = prev_y + num_steps * math.sin(angle)
        cur_r = math.sqrt(cur_x**2 + cur_y**2)
        cur_theta = math.atan2(cur_y, cur_x)
        if cur_gen == 3:
            cur_node = Node(lst[count], cur_theta, cur_r, 0, num_steps, cur_gen)
        elif cur_r > 5:
            cur_node = Node(lst[count], cur_theta, cur_r, 2, num_steps, cur_gen)
        else:
            cur_node = Node(lst[count], cur_theta, cur_r, random.randint(1, 10), num_steps, cur_gen)
        lst[count].next.append(cur_node)
        lst.append(cur_node)
    count += 1

for node in lst:
    plt.polar(node.theta_coord, node.r_coord, 'o', color=(0, 0, 0, 0.1))
    for kid in node.next:
        plt.polar([node.theta_coord, kid.theta_coord], [node.r_coord, kid.r_coord], color=(random.random(), random.random(), random.random(), 0.5))

plt.show()