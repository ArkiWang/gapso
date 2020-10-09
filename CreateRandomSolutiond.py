import numpy as np
def CreateRandomSolutiond(model):
    # 初始化种群
    n = model.n # 航迹点数量
    # x边界
    xmin = model.xmin
    xmax = model.xmax
    # 动态规划起点
    xst = model.xs
    yst = model.ys
    # y边界
    ymin = model.ymin
    ymax = model.ymax

    # 分层初始化
    x1 = np.random.uniform(xst - 1, (xst + xmax) / 2, (1, 3))
    y1 = np.random.uniform(yst - 1, (yst + ymax) / 2, 1, 3)
    x2 = np.random.uniform((xst + xmax) / 2, xmax, (1, n - 3))
    y2 = np.random.uniform((yst + ymax) / 2, ymax, (1, n - 3))

    # 随机初始化
    # sol1.x = unifrnd(xst, xmax, 1, n)
    # sol1.y = unifrnd(yst, ymax, 1, n)
    # 输出初始化航迹点

    x = [x1, x2]
    y = [y1, y2]
    return np.sort(x), np.sort(y)
