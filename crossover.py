from numpy import size, ones
import numpy as np

def crossover(sol1, sol2) -> tuple:
    pc = 0.7
    (x1,y1) = sol1
    (x2,y2) = sol2


    py = len(x1)

    x1 = list(x1); y1 = list(y1)
    x2 = list(x2); y2 = list(y2)

    newx1 = []
    newx2 = []
    newy1 = []
    newy2 = []
    rand = np.random.random()
    if (rand < pc):
        cpoint = round(rand * py)
        newx1 = x1[0:cpoint] + x2 [cpoint : py]
        newx2 = x2[0:cpoint] + x1 [cpoint : py]
        newy1 = y1[0:cpoint ] + y2 [cpoint : py]
        newy2 = y2[0:cpoint ] + y1 [cpoint : py]
    else:
        newx1 = x1
        newx2 = x2
        newy1 = y1
        newy2 = y2


    sol1 = (newx1, newy1)
    sol2 = (newx2, newy2)
    return (sol1, sol2)