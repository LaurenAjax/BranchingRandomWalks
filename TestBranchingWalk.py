import random
import copy
import matplotlib.pyplot as plot

class Node:
    def __init__(self, parent, x_coord, y_coord):
        self.parent = parent
        # this node's parent node
        self.x_coord = x_coord
        # all x-coordinates up to and including this node's
        self.y_coord = y_coord
        # all y-coordinates up to and including this node's
        self.left = None
        # the left kid of this node
        self.right = None
        # the right kid of this node

x = [0]
# the array of x-coordinates with only the starting x-coordinate
y = [0]
# the array of y-coordinates with only the starting y-coordinate
steps = 10
# the number of generations this tree will have
root = Node(None, x, y)
# the starting node from which all subsequent nodes are generated

def brancher(prev_node, count):
    if (count == steps):
        plot.plot(prev_node.x_coord, prev_node.y_coord, color=(0, 0, 0, 0.1))
        # plots the branch of the tree once it has terminated
        plot.plot(prev_node.x_coord[count - 1], prev_node.y_coord[count - 1], 'o', color=(0, 0, 0, 0.1))
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
            x_cur.append(x_cur[count - 1])
            y_cur.append(y_cur[count - 1] + 1)
        elif random_value == 2:
            # moves the kid node right
            x_cur.append(x_cur[count - 1] + 1)
            y_cur.append(y_cur[count - 1])
        elif random_value == 3:
            # moves the kid node down
            x_cur.append(x_cur[count- 1])
            y_cur.append(y_cur[count - 1] - 1)
        else:
            # moves the kid node left
            x_cur.append(x_cur[count - 1] - 1)
            y_cur.append(y_cur[count - 1])
        count += 1
        # increases the count of the generation by 1
        cur_node = Node(prev_node, x_cur, y_cur)
        # creates the kid node with its x and y coordinates appended onto their respective lists
        cur_node.left = brancher(cur_node, count)
        # generates the current node's left kid
        cur_node.right = brancher(cur_node, count)
        # generates the current node's right kid
        return cur_node
        # returns the current node to be added to its parent node's kids

root.left = brancher(root, 1)
# generates the root node's left kid
root.right = brancher(root, 1)
# generates the root node's right kid

plot.show()
# displays the plot