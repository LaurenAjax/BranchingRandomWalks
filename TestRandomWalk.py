import random
import matplotlib.pyplot as plot

colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
# an array of different colors
steps = 1000000
# the number of steps the random walk takes

for shade in colors:
    x = [0]
    # the array of x-coordinates with only the starting x-coordinate
    y = [0]
    # the array of y-coordinates with only the starting y-coordinate
    for i in range(1, steps):
        random_value = random.randint(1, 4)
        if random_value == 1:
            # moves the kid node up
            x.append(x[i - 1])
            y.append(y[i - 1] + 1)
        elif random_value == 2:
            # moves the kid node right
            x.append(x[i - 1] + 1)
            y.append(y[i - 1])
        elif random_value == 3:
            # moves the kid node down
            x.append(x[i - 1])
            y.append(y[i - 1] - 1)
        else:
            # moves the kid node left
            x.append(x[i - 1] - 1)
            y.append(y[i - 1])
    plot.plot(x, y, color=shade)
    # plots the walk in its entirety

plot.show()
# displays the plot