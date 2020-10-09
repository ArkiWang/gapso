from math import sqrt

import scipy.io as io
from gapso import gapso
from CreateModel import Model
def CreateModeld():
    # ptdx = load('kr.mat', 'ksi_sta_eta_x')
    # ptdy = load('kr.mat', 'ksi_sta_eta_y')
    # 起点
    xoyo = gapso()
    # 静态规划获得静态航迹及时间轴
    # 输入静态航迹数据
    x0 = xoyo.x0
    y0 = xoyo.y0
    T0 = xoyo.T0
    # 创建环境
    x1 = []
    y1 = []
    rd = 0.75 * 1   # r值修改位置
    d = 5
    t = 10
    # 输入卡尔曼预测数据
    a = io.loadmat('kr.mat')
    b = io.loadmat('kr.mat')
    dt =io.loadmat('dt.mat')   # 输入博弈移动威胁预测概率图
    ptdx = a.ksi_sta_eta_x
    ptdy = b.ksi_sta_eta_y

    # a = load('dt2.mat', 'CM_id_x2')
    # b = load('dt2.mat', 'CM_id_y2')
    # ptdx = a.CM_id_x2
    # ptdy = b.CM_id_y2
    # model.ptdx = a.CM_id_x2
    # model.ptdy = b.CM_id_y2
    # 判断无人机发现移动威胁
    while d > rd + 1.5:
        t = t + 1
        if t <= 150:
            xd = ptdx[t - 10]
            yd = ptdy[t - 10]
        elif 150 < t and t < 290:
             xd = ptdx[290 - t]
             yd = ptdy[290 - t]
        elif t > 289 and t < 400:
            xd = ptdx[t - 280]
            yd = ptdx[t - 280]
        elif t > 400:
            pass
        d = sqrt((x0[t] - xd)** 2 + (y0[t] - yd)**2)

    # 确定规划起点
    xs = x0[t]
    ys = y0[t]
    # 终点
    xt = 10
    yt = 10
    T = 0
    # 静态威胁构建
    xobs = [9, 2, 5, 7, 6, 3]
    yobs = [6, 7, 5, 2, 8, 3]
    robs = 1 * [1.5, 1.5, 1, 1, 1.2, 1.2]   # r值修改位置
    # 存储完成的静态航迹
    x1 = [x1, xs]
    y1 = [y1, ys]
    n = 4

    xmin = 0
    xmax = 10

    ymin = 0
    ymax = 10
    # 输出参数及数据
    model :Model
    model.x0 = x0
    model.y0 = y0
    model.x1 = x1
    model.y1 = y1
    model.t0 = t
    model.t1 = t
    Pl = 0.4
    Pt = 0.4
    Pdt = 0.1
    Pv = 0.1
    model.Pl = Pl
    model.Pt = Pt
    model.Pdt = Pdt
    model.Pv = Pv
    model.xs = xs
    model.ys = ys
    model.xt = xt
    model.yt = yt
    model.xobs = xobs
    model.yobs = yobs
    model.robs = robs
    model.rd = rd
    model.n = n
    model.xmin = xmin
    model.xmax = xmax
    model.ymin = ymin
    model.ymax = ymax

    model.ptdx = a.ksi_sta_eta_x
    model.ptdy = b.ksi_sta_eta_y
    model.dt = dt.dt
    return model