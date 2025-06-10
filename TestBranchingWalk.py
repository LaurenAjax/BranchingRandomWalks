import random
import copy
import matplotlib.pyplot as plot

class Node:
    def __init__(self, parent, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.parent = None
        self.left = None
        self.right = None

x = [0]
y = [0]
steps = 10
root = Node(None, x, y)

def brancher(prev_node, count):
    if (count == steps):
        plot.plot(prev_node.x_coord, prev_node.y_coord, color='k')
        return None
    else:
        x_cur = copy.deepcopy(prev_node.x_coord)
        y_cur = copy.deepcopy(prev_node.y_coord)
        random_value = random.randint(1, 4)
        if random_value == 1:
            x_cur.append(x_cur[count - 1])
            y_cur.append(y_cur[count - 1] + 1)
        elif random_value == 2:
            x_cur.append(x_cur[count - 1] + 1)
            y_cur.append(y_cur[count - 1])
        elif random_value == 3:
            x_cur.append(x_cur[count- 1])
            y_cur.append(y_cur[count - 1] - 1)
        else:
            x_cur.append(x_cur[count - 1] - 1)
            y_cur.append(y_cur[count - 1])
        count += 1
        cur_node = Node(prev_node, x_cur, y_cur)
        cur_node.left = brancher(cur_node, count)
        cur_node.right = brancher(cur_node, count)
        return cur_node

root.left = brancher(root, 1)
root.right = brancher(root, 1)

plot.show()