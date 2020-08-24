
import numpy as np
from numpy import sort

from CreateModel import Model
def CreateRandomSolution(model:Model) ->tuple:
    # 初始化种群
    n = model.n # 航迹点数量
    # 起点
    xs = model.xs
    ys = model.ys
    # x边界
    xmin = model.xmin
    xmax = model.xmax
    # y边界
    ymin = model.ymin
    ymax = model.ymax
    # 初始化并输出
    x = np.random.uniform(xs, xmax, (1, n))
    y = np.random.uniform(ys, ymax, (1, n))
    rx = sort(x)
    ry = sort(y)
    return (rx,ry)