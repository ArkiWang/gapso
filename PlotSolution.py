import matplotlib.pyplot as plt
from torch import numel, linspace, cos, sin
import numpy as np
from CreateModel import Model
def PlotSolution(sol, model:Model) -> None:
    xs = model.xs
    ys = model.ys
    xt = model.xt
    yt = model.yt
    xobs = model.xobs
    yobs = model.yobs
    robs = model.robs

    XS = sol.XS
    YS = sol.YS
    xx = sol.xx
    yy = sol.yy

    a = np.zeros((6, 3))
    a[0] = [1, 0, 0]
    a[1] = [1, 0, 0]
    a[2] = [0, 1, 0]
    a[3] = [0, 1, 0]
    a[4] = [0, 0, 1]
    a[5] = [0, 0, 1]

    theta = linspace(0, 2 * np.pi, 100)
    plt.figure()
    plt.xlim([0, 12])
    plt.ylim([0, 12])
    for k in range(len(xobs)):
        plt.fill(xobs[k] + robs[k] * cos(theta), yobs[k] + robs[k] * sin(theta), a[k])
        #hold on

    # daspect([1 1 1])
    plt.plot(xx, yy)
    plt.plot(XS, YS)
    plt.plot(xs, ys)
    plt.plot(xt, yt)

    plt.show()



