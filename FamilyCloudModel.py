import matplotlib.pyplot as plt
import random
import math

class Node:
    def __init__(self, parent, angle, theta_coord, r_coord, num_kids, steps, gen):
        self.parent = parent
        self.angle = angle
        self.theta_coord = theta_coord
        self.r_coord = r_coord
        self.upper_bound = 0
        self.lower_bound = 0
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
        if i == 0 and node.parent == None:
            angle = random.randint(1, 360)
        elif i == 0:
            node.upper_bound = node.angle + 90
            node.lower_bound = node.angle - 90
            angle = random.randint(node.lower_bound, node.upper_bound)
        elif node.parent == None:
            angle = random.randint(node.next[0].angle - 5, node.next[0].angle + 5)
        else:
            top = node.next[0].angle + 5
            bottom = node.next[0].angle - 5
            if bottom < node.lower_bound:
                bottom = node.lower_bound
            if top > node.upper_bound:
                top = node.upper_bound
            if top == node.upper_bound and top <= bottom:
                bottom = top - 5
            if bottom == node.lower_bound and bottom >= top:
                top = bottom + 5
            angle = random.randint(bottom, top)
        if node.parent != None:
            if node.parent.parent != None:
                for grandparent in node.parent.parent.next:
                    if grandparent is not node.parent:
                        for auncle in grandparent.next:
                            if angle < auncle.upper_bound and angle > auncle.lower_bound:
                                up = auncle.upper_bound - angle
                                down = angle - auncle.lower_bound
                                if up > down:
                                    angle = angle + up + random.randint(1, 5)
                                else:
                                    angle = angle - down - random.randint(1, 5)
                            for cousin in auncle.next:
                                node_x = prev_x + steps * math.cos(math.radians(angle))
                                node_y = prev_y + steps * math.sin(math.radians(angle))
                                cousin_x = cousin.r_coord * math.cos(cousin.theta_coord)
                                cousin_y = cousin.r_coord * math.sin(cousin.theta_coord)
                                distance = math.sqrt((node_x - cousin_x)**2 + (node_y - cousin_y)**2)
                                if distance < 2:
                                    if steps < 4:
                                        steps += 2
                                    else:
                                        steps -= 2
        cur_x = prev_x + steps * math.cos(math.radians(angle))
        cur_y = prev_y + steps * math.sin(math.radians(angle))
        cur_r = math.sqrt(cur_x**2 + cur_y**2)
        cur_theta = math.atan2(cur_y, cur_x)
        if cur_gen == 8:
            cur_node = Node(node, angle, cur_theta, cur_r, 0, steps, cur_gen)
        elif cur_r > 5:
            cur_node = Node(node, angle, cur_theta, cur_r, 2, steps, cur_gen)
        else:
            cur_node = Node(node, angle, cur_theta, cur_r, random.randint(1, 10), steps, cur_gen)
        node.next.append(cur_node)
        lst.append(cur_node)
    sort(node.next)
    count += 1

for node in lst:
    for kid in node.next:
        plt.polar([node.theta_coord, kid.theta_coord], [node.r_coord, kid.r_coord], color=(random.random(), random.random(), random.random(), 0.1))

plt.show()
# displays the plot