import math
import random
import matplotlib.pyplot as plot
import matplotlib.colors as color

class AAC:
    arr = []
    def increment(self, key):
        for p in self.arr:
            if p[0] == key:
                p[1] += 1
                return
        self.arr.append([key, 1])
    def get_val(self, key):
        for p in self.arr:
            if p[0] == key:
                return p[1]
        return 0
    def get_keys(self):
        output = []
        for p in self.arr:
            output.append(p[0])
        return output
    def get_max_val(self):
        output = 0
        for p in self.arr:
            output = max(p[1],output)
        return output
    
class node:
    loc = [0, 0]
    children = []
    parent = 0
    def __init__(self, pos, par):
        self.loc = pos.copy()
        # for val in pos:
        #     loc.append(val + 0)
        self.children = []
        self.parent = par
    def add_child(self, child):
        self.children.append(child)
    def wander_me(self):
        val = random.randint(0, 3)
        delta = [val%2*pow(-1,math.floor(val/2)), (val+1)%2*pow(-1,math.floor(val/2))]
        for i in range(2):
            self.loc[i] += delta[i]
        # print("(",self.loc[0],", ",self.loc[1],")")
    def wander(self,num):
        if num == 1:
            self.wander_me()
        else:
            for child in self.children:
                child.wander(num - 1)
    def propogate_me(self):
        for i in range(2):
            self.add_child(node(self.loc, self))
    def propogate(self, num):
        if num == 0:
            # print("Propogating self")
            self.propogate_me()
            for child in self.children:
                child.wander_me()
        else:
            for child in self.children:
                # print("Propogating child with num = ",num - 1)
                child.propogate(num - 1)
    def plot_path(self, arr):
        arr[0].append(self.loc[0])
        arr[1].append(self.loc[1])
        for child in self.children:
            child.plot_path(arr)
        if self.children == []:
            plot.plot(arr[0], arr[1], color=(random.random(),random.random(),random.random()))
            plot.plot([arr[0].pop()], [arr[1].pop()], 'o', color=(random.random(),random.random(),random.random()))
        else:
            arr[0].pop()
            arr[1].pop()
    def gen_dist_helper(self, aac):
        if self.children == []:
            aac.increment(self.loc)
        else:
            for child in self.children:
                child.gen_dist_helper(aac)

    def gen_dist(self):
        arr = AAC()
        self.gen_dist_helper(arr)
        keys = arr.get_keys()
        max = arr.get_max_val()
        xArr = []
        yArr = []
        cArr = []
        for k in keys:
            xArr.append(k[0])
            yArr.append(k[1])
            cArr.append(color.hsv_to_rgb(((arr.get_val(k)/max)*5/6,1,1)))
        plot.scatter(xArr, yArr, c=cArr)

root = node([0,0], 0)
# print("Running")
for i in range(10):
    # print("Running with i =",i)
    root.propogate(i)
# root.plot_path([[],[]])
plot.axis([-10, 10, -10, 10])
plot.grid(True)
ticks = []
for i in range(21):
    ticks.append(i-10)
plot.xticks(ticks)
plot.yticks(ticks)
root.gen_dist()
plot.show()
# print("Terminating")