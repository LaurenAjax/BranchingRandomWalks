import random
import matplotlib.pyplot as plot
import math

class Node:
    def __init__(self, parent, theta_coord, r_coord, num_kids, gen):
        self.parent = parent
        # this node's parent node
        self.theta_coord = theta_coord
        # the degree at which this node's point is angled from the origin (in radians)
        self.r_coord = r_coord
        # the distance this node's point is from the origin
        self.num_kids = num_kids
        # the number of kids this node has
        self.next = []
        # an array of nodes containing all this node's kids
        self.gen = gen
        # the number of nodes away from the starting node this node is

root = Node(None, 0, 0, random.randint(0, 10), 0)
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
    for i in range(node.num_kids):
    # generates all of the parent's kids
        random_value = random.randint(1, 22)
        # a random value whose outcome determines the direction in which the kid node goes
        if (node.parent != None):
        # checks whether or not the parent node is the first node
            if random_value < 22:
                angle = math.radians(random.randint(int(math.degrees(prev_theta)) - 10 - cur_gen, int(math.degrees(prev_theta)) + 10 + cur_gen))
                # determines the degree to which the angle of the kid node varies from it's
                # parent's angle, with the variation increasing with the generation
            else:
                angle = math.radians(random.randint(1, 360))
                # enables a small chance for the node to go off in a completely random direction
        else:
            if random_value < 8:
                angle = math.radians(random.randint(-10, 10))
                # gives a roughtly one-third chance for the angle to be centered around degree 0
            elif random_value < 15:
                angle = math.radians(random.randint(110, 130))
                # gives a roughly one-third chance for the angle to be centered around degree 120
            elif random_value < 22:
                angle = math.radians(random.randint(230, 250))
                # gives a roughly one-third chance for the angle to be centered around degree 240
            else:
                angle = math.radians(random.randint(1, 360))
                # enables a small chance for the node to go off in a completely random direction
        cur_x = prev_x + math.cos(angle)
        # produces the x-coordinate of the kid node
        cur_y = prev_y + math.sin(angle)
        # produces the y-coordinate of the kid node
        cur_r = math.sqrt(cur_x**2 + cur_y**2)
        # produces the distance from the origin to the kid node
        cur_theta = math.atan2(cur_y, cur_x)
        # produces the angle the kid node has from the origin
        if cur_gen == 10:
            cur_node = Node(node, cur_theta, cur_r, 0, cur_gen)
            # prevents further kids from being born after the tenth generation
        else:
            cur_node = Node(node, cur_theta, cur_r, random.randint(0, 4), cur_gen)
            # forms the kid node that will have a random number of kids in turn
        node.next.append(cur_node)
        # adds the kid node to the parent node's array of kids
        lst.append(cur_node)
        # adds the kid node to the list of all nodes in the tree
    count += 1
    # increases the index currently being referenced by 1

for node in lst:
    plot.polar(node.theta_coord, node.r_coord, 'o', color=(0, 0, 0, 0.1))
    # plots a transparent black dot at the polar coordinates of all the nodes
    for kid in node.next:
        plot.polar([node.theta_coord, kid.theta_coord], [node.r_coord, kid.r_coord], color=(random.random(), random.random(), random.random(), 0.5))
        # plots a randomly colored line between a parent node and each one of their kid nodes

plot.show()
# displays the plot