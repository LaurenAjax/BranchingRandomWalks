import random
import matplotlib.pyplot as plot
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
steps = 1000000
for shade in colors:
    x = [0]
    y = [0]
    for i in range(1, steps):
        random_value = random.randint(1, 4)
        if random_value == 1:
            x.append(x[i - 1])
            y.append(y[i - 1] + 1)
        elif random_value == 2:
            x.append(x[i - 1] + 1)
            y.append(y[i - 1])
        elif random_value == 3:
            x.append(x[i - 1])
            y.append(y[i - 1] - 1)
        else:
            x.append(x[i - 1] - 1)
            y.append(y[i - 1])
    plot.plot(x, y, color=shade)
plot.show()
