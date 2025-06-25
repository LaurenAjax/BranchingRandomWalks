import matplotlib.pyplot as plt
import random
import math

class Node:
    def __init__(self, parent, angle, theta_coord, r_coord, num_kids, steps, gen):
        self.parent = parent
        # this node's parent node
        self.angle = angle
        # this node's angle from it's parent (in radians)
        self.theta_coord = theta_coord
        # the degree at which this node's point is angled from the origin (in radians)
        self.r_coord = r_coord
        # the distance this node's point is from the origin
        self.num_kids = num_kids
        # the number of kids this node has
        self.next = []
        # an array of nodes containing all this node's kids
        self.steps = steps
        # the number of steps this node took before having kids
        self.gen = gen
        # the number of nodes away from the starting node this node is

def sort(arr):
# sorts the given array from smallest value to largest
    for i in range(1, len(arr)):
        for j in range(i - 1, -1, -1):
            if arr[j + 1].angle < arr[j].angle:
                temp = arr[j + 1]
                arr[j + 1] = arr[j]
                arr[j] = temp

def order(node): 
# splits the array and reconcatenates it so that the middlemost element is first
    counter = len(node.next) // 2
    sort(node.next)
    first_list = node.next[:counter]
    second_list = node.next[counter:]
    node.next = second_list + first_list

root = Node(None, 0, 0, 0, random.randint(1, 10), random.randint(1, 5), 0)
# the starting node from which all subsequent nodes are generated
lst = [root]
# a list containing all nodes that make up the tree
count = 0
# the current index we are on in the list

while count < len(lst):
# visits all nodes and gives them kids
    node = lst[count]
    cur_gen = node.gen + 1
    # the current number of nodes we are away from the origin
    prev_r = node.r_coord
    # the parent node's distance from the origin
    prev_theta = node.theta_coord
    # the parent node's angle from the origin
    prev_x = prev_r * math.cos(prev_theta)
    # the parent node's x-coordinate on the xy-plane
    prev_y = prev_r * math.sin(prev_theta)
    # the parent node's y-coordinate on the xy-plane
    steps = random.randint(1, 5)
    # the number of steps the kid nodes will move before having kids
    for i in range(node.num_kids):
    # generates all of the parent's kids
        if i == 0 and node.parent == None:
        # assigns a value to the first kid of a parent who doesn't have a parent
            angle = random.randint(1, 360)
            # a random value whose outcome is the degree in which the kid node goes
        elif i == 0:
        # assigns a value to the first kid of a parent who has a parent
            for j in range(node.parent.num_kids):
                if node.parent.next[j] is node:
                    angle = random.randint((360 // node.parent.num_kids) * j + node.angle - 5, (360 // node.parent.num_kids) * j + node.angle + 5)
                    # makes the cousins equidistant from each other (for maximum repulsion) according to parent birth order
        else:
            angle = random.randint(node.next[0].angle - 5, node.next[0].angle + 5)
            # keeps the siblings close to their eldest
        cur_x = prev_x + steps * math.cos(math.radians(angle))
        # produces the x-coordinate of the kid node
        cur_y = prev_y + steps * math.sin(math.radians(angle))
        # produces the y-coordinate of the kid node
        cur_r = math.sqrt(cur_x**2 + cur_y**2)
        # produces the distance from the origin to the kid node
        cur_theta = math.atan2(cur_y, cur_x)
        # produces the angle the kid node has from the origin
        if cur_gen == 5:
            cur_node = Node(node, angle, cur_theta, cur_r, 0, steps, cur_gen)
            # prevents further kids from being born after the third generation
        elif cur_r > 5:
            cur_node = Node(node, angle, cur_theta, cur_r, 2, steps, cur_gen)
            # has exactly two kids when greater than distance 5 away from the origin
        else:
            cur_node = Node(node, angle, cur_theta, cur_r, random.randint(1, 10), steps, cur_gen)
            # has in between one and ten kids when distance 5 or less from the origin
        node.next.append(cur_node)
        # adds the kid node to the parent node's array of kids
        lst.append(cur_node)
        # adds the kid node to the list of all nodes in the tree
    order(node)
    # orders the kids to ensure cousins don't intersect
    count += 1
    # increases the index currently being referenced by 1

for node in lst:
    plt.polar(node.theta_coord, node.r_coord, 'o', color=(0, 0, 0, 0.01))
    # plots a transparent black dot at the polar coordinates of all the nodes
    for kid in node.next:
        plt.polar([node.theta_coord, kid.theta_coord], [node.r_coord, kid.r_coord], color=(random.random(), random.random(), random.random(), 0.5))
        # plots a randomly colored line between a parent node and each one of their kid nodes

plt.show()
# displays the plot