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
    dir = 0
    dir_var = 0
    mirror_var = 0
    self_var = 0
    fineness = 1
    generation = 1
    
    def __init__(self, pos, par, theta, phi, sigma, delta, rho, fin, gen):
        self.loc = pos.copy()
        self.children = []
        self.parent = par
        self.fineness = fin
        self.dif = phi
        if self.parent == None:
            self.dir = theta * 2 * math.pi / 360
            self.dir_var = sigma * self.fineness
            self.mirror_var = delta * self.fineness
            self.self_var = rho * self.fineness
        else:
            self.dir = theta
            self.dir_var = sigma
            self.mirror_var = delta
            self.self_var = rho
        self.generation = gen
        
    def add_child(self, child):
        self.children.append(child)
        
    def wander_me(self, thetaA, thetaB):
        thetaC = random.randint(-self.self_var - self.generation, self.self_var + self.generation) * 2 / self.fineness * math.pi / 360
        self.dir += thetaA + thetaB + thetaC
        delta = [math.cos(self.dir), math.sin(self.dir)]
        for i in range(2):
            self.loc[i] += delta[i]
        # print("(",self.loc[0],", ",self.loc[1],")")
    
    def wander(self,num):
        if num == 1:
            self.wander_me(0, 0)
        if num == 2:
            thetaA = random.randint(-self.dir_var - self.generation, self.dir_var + self.generation) * 2 / self.fineness * math.pi / 360 
            thetaB = random.randint(-self.mirror_var - self.generation, self.mirror_var + self.generation) * 2 / self.fineness * math.pi / 360
            for i in range(len(self.children)):
                self.children[i].wander_me(thetaA*pow(-1,i),thetaB)
        else:
            for child in self.children:
                child.wander(num - 1)
    
    def propogate_me(self):
        for i in range(2):
            self.add_child(node(self.loc, self, self.dir + self.dif*math.pow(-1,i) * 2 * math.pi / 360, self.dif, self.dir_var, self.mirror_var, self.self_var, self.fineness, self.generation + 1))
    
    def propogate(self, num):
        if num == 0:
            # print("Propogating self")
            self.propogate_me()
            self.wander(2)
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
            plot.plot(arr[0], arr[1], color=(random.random(),random.random(),random.random(),1))
            plot.plot([arr[0].pop()], [arr[1].pop()], 'o', color=(random.random(),random.random(),random.random(),1))
        else:
            arr[0].pop()
            arr[1].pop()
    
    def gen_dist_helper(self, aac, num):
        if num == 0:
            aac.increment(self.loc)
        else:
            for child in self.children:
                child.gen_dist_helper(aac, num - 1)

    def gen_dist(self, num):
        arr = AAC()
        self.gen_dist_helper(arr, num)
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
        print(max)

root = node([0,0], None, 0, 16, 8, 4, 2, 1, 1)
# rootA = node([0,0], None, 90, 16, 8, 4, 2, 1, 1)
# rootB = node([0,0], None, 180, 16, 8, 4, 2, 1, 1)
# rootC = node([0,0], None, 270, 16, 8, 4, 2, 1, 1)
# print("Running")
gen = 10
for i in range(gen):
    # print("Running with i =",i)
    root.propogate(i)
    # rootA.propogate(i)
    # rootB.propogate(i)
    # rootC.propogate(i)

plot.axis([-gen, gen, -gen, gen])
plot.grid(True)
ticks = []
for i in range(3):
    ticks.append(gen*i-gen)
plot.xticks(ticks)
plot.yticks(ticks)

root.plot_path([[],[]])
# rootA.plot_path([[],[]])
# rootB.plot_path([[],[]])
# rootC.plot_path([[],[]])
# root.gen_dist(gen)
plot.show()
# print("Terminating")