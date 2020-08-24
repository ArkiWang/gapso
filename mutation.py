 # 变异
from numpy import size
import numpy as np
def mutation(sol1) -> tuple:
    pm = 0.006   # 变异概率
    # 输入航迹
    (x1, y1) = sol1

    # 创建存储空间
    py = len(x1)
    newx = x1
    newy = y1
    newx = list(newx)
    newy = list(newy)
    rand = np.random.random()
    mpoint = 0
    # 进行变异
    if (rand < pm):
        mpoint = round(rand * py)
        if (mpoint == 0):  # 起点不能变异
            mpoint = mpoint + 1
    newx[mpoint] = round(rand * py)
    newy[mpoint] = round(rand * py)
    # 输出新航迹
    return (newx, newy)


