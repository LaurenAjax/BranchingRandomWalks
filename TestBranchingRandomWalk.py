import random
import copy
import matplotlib.pyplot as plot

class Node:
    def __init__(self, parent, x_coord, y_coord, num_kids, gen):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.parent = None
        self.num_kids = num_kids
        self.next = []
        self.gen = gen
        

x = [0]
y = [0]
root = Node(None, x, y, random.randint(0, 5), 1)

def brancher(prev_node):
    if (prev_node.num_kids == 0 or prev_node.gen == 10):
        plot.plot(prev_node.x_coord, prev_node.y_coord, color=(0, 0, 0, 0.3))
        plot.plot(prev_node.x_coord[len(prev_node.x_coord) - 1], prev_node.y_coord[len(prev_node.y_coord) - 1], 'o', color=(0, 0, 0, 0.3))
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
        cur_node = Node(prev_node, x_cur, y_cur, random.randint(0, 5), prev_node.gen + 1)
        for i in range(prev_node.num_kids):
            cur_node.next.append(brancher(cur_node))
        return cur_node

for i in range(root.num_kids):
    root.next.append(brancher(root))

plot.show()