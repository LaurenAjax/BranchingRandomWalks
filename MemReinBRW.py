import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color
import functools as ft

def to_unit(arr):
    scale = 0
    output = []
    for i in arr:
        scale += i*i
    scale = math.sqrt(scale)
    if scale > 0.001:
        for j in range(len(arr)):
            output.append(arr[j] / scale)
    else:
        for j in range(len(arr)):
            output.append(0)
    return output

def scale_arr(arr, scale):
    output = []
    for i in range(len(arr)):
        output.append(arr[i] * scale)
    return output
        
def arr_dif(arrA, arrB):
    output = []
    for i in range(len(arrA)):
        output.append(arrA[i] - arrB[i])
    return output

class Node:
    true_pos = [0, 0]
    init_pos = [0, 0]
    delta_pos = [0, 0]
    parent = None
    children = []
    step_len = 1
    weights = [1, 1, 1]
    
    def __init__(self, pos, delta, par, len, weight):
        self.init_pos = pos
        self.delta_pos = delta
        self.step_len = len
        self.true_pos = [0, 0]
        self.calcTruePos()
        self.parent = par
        self.weights = weight
        self.children = []
        
    def calcTruePos(self):
        for i in range(2):
            self.true_pos[i] = self.init_pos[i] + self.delta_pos[i] * self.step_len * random.randint(1,3) / 2
    
    def relation_movement(self):
        cousin_arr = []
        sibling_arr = []
        if self.parent is not None:
            grand_par = self.parent.parent
            if grand_par is not None:
                for uncle in grand_par.children:
                    if uncle is self.parent:
                        for sibling in uncle.children:
                            if sibling is not self:
                                sibling_arr.append(sibling)
                    else:
                        for cousin in uncle.children:
                            cousin_arr.append(cousin)
            else:
                for sibling in self.parent.children:
                    if sibling is not self:
                        sibling_arr.append(sibling)
            # sibling_pull = ft.reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], map(lambda x: scale_arr(arr_dif(x.true_pos, self.true_pos), pow(self.dist_to(x.true_pos), 2)), sibling_arr), [0, 0])
            # cousin_push = ft.reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], map(lambda x: scale_arr(arr_dif(x.true_pos, self.true_pos), pow(self.dist_to(x.true_pos), 2)), cousin_arr), [0, 0])
            sibling_pull = ft.reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], map(lambda x: arr_dif(x.true_pos, self.true_pos), sibling_arr), [0, 0])
            cousin_push = ft.reduce(lambda x, y: [x[0] + y[0], x[1] + y[1]], map(lambda x: arr_dif(x.true_pos, self.true_pos), cousin_arr), [0, 0])
            sibling_pull = to_unit(sibling_pull)
            cousin_push = to_unit(cousin_push)
            for i in range(2):
                self.delta_pos[i] = self.delta_pos[i] * self.weights[0] + sibling_pull[i] * self.weights[1] + cousin_push[i] * self.weights[2]
            self.delta_pos = to_unit(self.delta_pos)

    def inv_dist_to(self, arr):
        result = self.dist_to(arr)
        if result == 0:
            return 0
        return 1 / result
    
    def dist_to(self, arr):
        return math.sqrt(math.pow(arr[0] - self.true_pos[0], 2) + math.pow(arr[1] - self.true_pos[1], 2))
    
    def new_gen(self):
        if self.dist_to([0, 0]) < 5:
            count = random.randint(1, 10)
        else:
            count = 2
        for i in range(count):
            dir = math.radians(random.randint(1, 360))
            self.children.append(Node(self.true_pos, [math.cos(dir),math.sin(dir)], self, self.step_len, self.weights))
    
    def propogate(self, num):
        if num == 0:
            self.new_gen()
        elif num == 1:
            for child in self.children:
                child.new_gen()
            for child in self.children:
                for grandchild in child.children:
                    grandchild.relation_movement()
                for grandchild in child.children:
                    grandchild.calcTruePos()
        else:
            for child in self.children:
                child.propogate(num - 1)
    
    def run_gens(self, num, **kwargs):
        low = kwargs.get('last', 0)
        for i in range(low, num):
            print("Running gen", i+1, "/", num)
            self.propogate(i)
        print("Generation finished")
            
    def plot_path_helper(self, arr):
        arr[0].append(self.true_pos[0])
        arr[1].append(self.true_pos[1])
        for child in self.children:
            child.plot_path_helper(arr)
        if self.children == []:
            plot.plot(arr[0], arr[1], color=(0, 0, 0, .1))
            plot.plot([arr[0].pop()], [arr[1].pop()], 'o', color=(1, 0, 0, .1))
        else:
            arr[0].pop()
            arr[1].pop()
            
    def plot_path(self):
        self.plot_path_helper([[], []])
        
    def plot_singular_path_helper(self, arr):
        for child in self.children:
            child.plot_singular_path_helper(self.true_pos)
        plot.plot([arr[0], self.true_pos[0]], [arr[1], self.true_pos[1]], color=(0, 0, 0, .1))
        if self.children == []:
            plot.plot([self.true_pos[0]], [self.true_pos[1]], 'o', color=(1, 0, 0, .01))
    
    def plot_singular_path(self):
        for child in self.children:
            child.plot_singular_path_helper(self.true_pos)


step_length = 1
root = Node([0, 0], [0, 0], None, step_length, [1, 1, -1])
gens = 10
root.run_gens(gens)
plot.axis([-gens * step_length, gens * step_length, -gens * step_length, gens * step_length])
plot.grid(True)
ticks = []
for i in range(2 * step_length + 1):
    ticks.append(gens * i * 1.5 - gens * step_length * 1.5)
plot.xticks(ticks)
plot.yticks(ticks)
root.plot_singular_path()
granularity = 360
for j in range(1, math.ceil(gens * step_length * 1.5 + 1)):
    circ_path = [[], []]
    for i in range(granularity):
        circ_path[0].append(j * math.cos(math.radians(360 * i / granularity)))
        circ_path[1].append(j * math.sin(math.radians(360 * i / granularity)))
    circ_path[0].append(j)
    circ_path[1].append(0)
    if j % 5 == 0:
        plot.plot(circ_path[0], circ_path[1], color = (0, 1, 0, 1))
    else:
        plot.plot(circ_path[0], circ_path[1], color = (0, 0, 1, 1))
plot.plot([0], [0], 'o', color = (0, 1, 0, 1))

plot.show()