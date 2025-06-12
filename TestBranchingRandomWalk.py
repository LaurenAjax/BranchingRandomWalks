import random
import copy
import matplotlib.pyplot as plot

class Node:
    def __init__(self, parent, x_coord, y_coord, num_kids):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.parent = None
        self.num_kids = num_kids
        self.next = []
        

x = [0]
y = [0]
root = Node(None, x, y, random.randint(0, 2))

def brancher(prev_node):
    if (prev_node.num_kids == 0):
        plot.plot(prev_node.x_coord, prev_node.y_coord, color=(random.random(),random.random(),random.random()))
        plot.plot(prev_node.x_coord[len(prev_node.x_coord) - 1], prev_node.y_coord[len(prev_node.y_coord) - 1], 'o', color='k')
        return None
    else:
        x_cur = copy.deepcopy(prev_node.x_coord)
        y_cur = copy.deepcopy(prev_node.y_coord)
        random_value = random.randint(1, 4)
        if random_value == 1:
            x_cur.append(x_cur[len(x_cur) - 1])
            y_cur.append(y_cur[len(y_cur) - 1] + 1)
        elif random_value == 2:
            x_cur.append(x_cur[len(x_cur) - 1] + 1)
            y_cur.append(y_cur[len(y_cur) - 1])
        elif random_value == 3:
            x_cur.append(x_cur[len(x_cur) - 1])
            y_cur.append(y_cur[len(y_cur) - 1] - 1)
        else:
            x_cur.append(x_cur[len(x_cur) - 1] - 1)
            y_cur.append(y_cur[len(y_cur) - 1])
        cur_node = Node(prev_node, x_cur, y_cur, random.randint(0, 2))
        for i in range(prev_node.num_kids):
            cur_node.next.append(brancher(cur_node))
        return cur_node

root.next = brancher(root)

plot.show()