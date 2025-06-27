import matplotlib.pyplot as plt
import random
import math

class Node:
    def __init__(self, parent, angle, theta_coord, r_coord, x_coord, y_coord, num_kids, gen):
        self.parent = parent
        self.angle = angle
        self.theta_coord = theta_coord
        self.r_coord = r_coord
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.num_kids = num_kids
        self.next = []
        self.gen = gen

root = Node(None, 0, 0, 0, 0, 0, random.randint(1, 10), 0)
lst = [root]
count = 0

while count < len(lst):
    node = lst[count]
    cur_gen = node.gen + 1
    prev_r = node.r_coord
    prev_theta = node.theta_coord
    prev_x = node.x_coord
    prev_y = node.y_coord
    steps = random.randint(1, 5)
    for i in range(node.num_kids):
        steps = random.randint(1, 5)
        angle = random.randint(1, 360)
        cur_x = prev_x + steps * math.cos(math.radians(angle))
        cur_y = prev_y + steps * math.sin(math.radians(angle))
        cur_r = math.sqrt(cur_x**2 + cur_y**2)
        cur_theta = math.atan2(cur_y, cur_x)
        r = cur_r
        theta = cur_theta
        check = 0
        for ln in lst:
            if math.sqrt((cur_x - ln.x_coord)**2 + (cur_y - ln.y_coord)**2) < 2:
                check += 1
                if check >= 5:
                    steps = random.randint(1, 5)
                    angle = random.randint(1, 360)
                    cur_x = prev_x + steps * math.cos(math.radians(angle))
                    cur_y = prev_y + steps * math.sin(math.radians(angle))
                    cur_r = math.sqrt(cur_x**2 + cur_y**2)
                    cur_theta = math.atan2(cur_y, cur_x)
        loop = 0
        while (cur_r != r or cur_theta != theta) and loop < 10:
            check = 0
            r = cur_r
            theta = cur_theta
            for ln in lst:
                if math.sqrt((cur_x - ln.x_coord)**2 + (cur_y - ln.y_coord)**2) < 2:
                    check += 1
                    if check >= 5:
                        steps = random.randint(1, 5)
                        angle = random.randint(1, 360)
                        cur_x = prev_x + steps * math.cos(math.radians(angle))
                        cur_y = prev_y + steps * math.sin(math.radians(angle))
                        cur_r = math.sqrt(cur_x**2 + cur_y**2)
                        cur_theta = math.atan2(cur_y, cur_x)
            loop += 1
        if cur_gen == 5:
            cur_node = Node(node, angle, cur_theta, cur_r, cur_x, cur_y, 0, cur_gen)
        elif cur_r > 5:
            cur_node = Node(node, angle, cur_theta, cur_r, cur_x, cur_y, 2, cur_gen)
        else:
            cur_node = Node(node, angle, cur_theta, cur_r, cur_x, cur_y, random.randint(1, 10), cur_gen)
        node.next.append(cur_node)
        lst.append(cur_node)
        plt.polar(cur_node.theta_coord, cur_node.r_coord, 'o', color=(0, 0, 0, 0.1))
    count += 1

plt.show()