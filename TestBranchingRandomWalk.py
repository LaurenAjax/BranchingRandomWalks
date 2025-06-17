import random
import copy
import matplotlib.pyplot as plot

class Node:
    def __init__(self, parent, x_coord, y_coord, num_kids, gen):
        self.parent = parent
        # this node's parent node
        self.x_coord = x_coord
        # all x-coordinates up to and including this node's 
        self.y_coord = y_coord
        # all y-coordinates up to and including this node's
        self.num_kids = num_kids
        # the number of kids this node has
        self.next = []
        # an array of nodes containing all this node's kids
        self.gen = gen
        # the number of nodes away from the starting node this node is      

x = [0]
# the array of x-coordinates with only the starting x-coordinate
y = [0]
# the array of y-coordinates with only the starting y-coordinate
root = Node(None, x, y, random.randint(0, 5), 1)
# the starting node from which all subsequent nodes are generated

def brancher(prev_node):
    if (prev_node.num_kids == 0 or prev_node.gen == 10):
        plot.plot(prev_node.x_coord, prev_node.y_coord, color=(0, 0, 0, 0.3))
        # plots the branch of the tree once it has terminated
        plot.plot(prev_node.x_coord[len(prev_node.x_coord) - 1], prev_node.y_coord[len(prev_node.y_coord) - 1], 'o', color=(0, 0, 0, 0.3))
        # plots the end point of the branch
        return None
        # returns a non-existent node in place of kid nodes
    else:
        x_cur = copy.deepcopy(prev_node.x_coord)
        # creates a distinct copy of the previous node's list of x-coordinates
        y_cur = copy.deepcopy(prev_node.y_coord)
        # creates a distinct copy of the previous node's list of y-coordinates
        random_value = random.randint(1, 4)
        # generates a random value that determines the direction the kid node travels
        if random_value == 1:
            # moves the kid node up
            x_cur.append(x_cur[len(x_cur) - 1])
            y_cur.append(y_cur[len(y_cur) - 1] + 1)
        elif random_value == 2:
            # moves the kid node right
            x_cur.append(x_cur[len(x_cur) - 1] + 1)
            y_cur.append(y_cur[len(y_cur) - 1])
        elif random_value == 3:
            # moves the kid node down
            x_cur.append(x_cur[len(x_cur) - 1])
            y_cur.append(y_cur[len(y_cur) - 1] - 1)
        else:
            # moves the kid node left
            x_cur.append(x_cur[len(x_cur) - 1] - 1)
            y_cur.append(y_cur[len(y_cur) - 1])
        cur_node = Node(prev_node, x_cur, y_cur, random.randint(0, 5), prev_node.gen + 1)
        # creates the kid node with its x and y coordinates appended onto their respective lists
        for i in range(cur_node.num_kids):
            cur_node.next.append(brancher(cur_node))
            # generates the current node's kids
        return cur_node
        # returns the current node to be added to its parent node's kids

for i in range(root.num_kids):
    root.next.append(brancher(root))
    # generates the root node's kids

plot.show()
# displays the plot