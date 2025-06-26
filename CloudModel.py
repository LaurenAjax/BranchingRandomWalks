import matplotlib.pyplot as plt
import random
import math

class Node:
    def __init__(self, parent, angle, theta_coord, r_coord, num_kids, steps, gen):
        self.parent = parent
        self.angle = angle
        self.theta_coord = theta_coord
        self.r_coord = r_coord
        self.num_kids = num_kids
        self.next = []
        self.steps = steps
        self.gen = gen

def sort(arr):
    for i in range(1, len(arr)):
        for j in range(i - 1, -1, -1):
            if arr[j + 1].angle < arr[j].angle:
                temp = arr[j + 1]
                arr[j + 1] = arr[j]
                arr[j] = temp

def order(node): 
    counter = len(node.next) // 2
    sort(node.next)
    first_list = node.next[:counter]
    second_list = node.next[counter:]
    node.next = second_list + first_list

root = Node(None, 0, 0, 0, random.randint(1, 10), random.randint(1, 5), 0)
lst = [root]
count = 0

while count < len(lst):
    node = lst[count]
    cur_gen = node.gen + 1
    prev_r = node.r_coord
    prev_theta = node.theta_coord
    prev_x = prev_r * math.cos(prev_theta)
    prev_y = prev_r * math.sin(prev_theta)
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
        for ln in lst:
            if abs(cur_r - ln.r_coord) > 3 and abs(cur_theta - ln.theta_coord) > 0.05:
                steps = random.randint(1, 5)
                angle = random.randint(1, 360)
                cur_x = prev_x + steps * math.cos(math.radians(angle))
                cur_y = prev_y + steps * math.sin(math.radians(angle))
                cur_r = math.sqrt(cur_x**2 + cur_y**2)
                cur_theta = math.atan2(cur_y, cur_x)
        loop = 0
        while (cur_r != r or cur_theta != theta) and loop < 5:
            r = cur_r
            theta = cur_theta
            for ln in lst:
                if abs(cur_r - ln.r_coord) > 3 and abs(cur_theta - ln.theta_coord) > 0.05:
                    steps = random.randint(1, 5)
                    angle = random.randint(1, 360)
                    cur_x = prev_x + steps * math.cos(math.radians(angle))
                    cur_y = prev_y + steps * math.sin(math.radians(angle))
                    cur_r = math.sqrt(cur_x**2 + cur_y**2)
                    cur_theta = math.atan2(cur_y, cur_x)
            loop += 1
        if cur_gen == 5:
            cur_node = Node(node, angle, cur_theta, cur_r, 0, steps, cur_gen)
        elif cur_r > 5:
            cur_node = Node(node, angle, cur_theta, cur_r, 2, steps, cur_gen)

        else:
            cur_node = Node(node, angle, cur_theta, cur_r, random.randint(1, 10), steps, cur_gen)
        node.next.append(cur_node)
        lst.append(cur_node)
    count += 1

for node in lst:
    plt.polar(node.theta_coord, node.r_coord, 'o', color=(0, 0, 0, 0.1))

plt.show()