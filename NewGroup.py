import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color
import functools as ft

plot.figure(figsize = [6, 6])

# directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]

def arr_sum(first_arr, second_arr):
    output = []
    for i in range(len(first_arr)):
        output.append(first_arr[i] + second_arr[i])
    return output

class Node:
    def __init__(self, loc, par):
        self.pos = loc
        self.parent = par
        self.children = []
    
    def make_children_helper(self, number):
        if number == 0:
            self.make_children()
        else:
            for child in self.children:
                child.make_children_helper(number - 1)
    
    def make_children(self):
        for i in range(2):
            number = random.random() * 2 * math.pi
            self.children.append(Node(arr_sum(self.pos, [math.cos(number), math.sin(number)]), self))
            plot.plot([self.pos[0], self.children[i].pos[0]], [self.pos[1], self.children[i].pos[1]])
        
    def run_gens(self, number):
        for i in range(number):
            self.make_children_helper(i)
            print("Finished generation",i)
            
    def f(self, t):
        return 2

root = Node([0, 0], None)
# history = [root]

generations = 20
ticks = []
for i in range(generations * 2 + 1):
    ticks.append(i - generations)
plot.axis([-generations, generations, -generations, generations])
plot.xticks(ticks)
plot.yticks(ticks)

# for gen in range(generations):
#     number = random.randint(0, 3)
#     history.append(Node(arr_sum(history[-1].pos, directions[number])))
#     plot.plot([history[-2].pos[0], history[-1].pos[0]], [history[-2].pos[1], history[-1].pos[1]])

root.run_gens(generations)



plot.show()