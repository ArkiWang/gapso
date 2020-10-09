from math import sqrt, ceil, atan2

from numpy import linspace, mean, rad2deg
from ParseSolution import Solution

def ParseSolutiond(sol1, model):
     # 输入航迹数据，环境数据
    x = sol1.x
    y = sol1.y
    t0 = model.t0
    t1 = model.t1
    xs = model.xs
    ys = model.ys
    xt = model.xt
    yt = model.yt
    xe = model.x1
    ye = model.y1

    xobs = model.xobs
    yobs = model.yobs
    robs = model.robs
    rd = model.rd
    ptdx = model.ptdx
    ptdy = model.ptdy
    dd = model.dd

    # 分配空间
    xx = []
    yy = []
    # 创建航迹空间参数
    vs = 0
    vdt = 0
    T = 0
    L = 0
    Violation = 0
    # xv = zeros(1, size(x))
    # yv = zeros(1, size(y))
    # 创建起点与航迹节点集 - 进行角度计算
    if len(xe) > 1:
        xv = [xe[len(xe) - 2], xe[len(xe) - 1], x]
        yv = [ye(len(ye) - 2), ye[len(ye) - 1], y]
    elif len(xe) == 1:
        xv = [xe[len(xe) - 1], x]
        yv = [ye[len(ye) - 1], y]
    # 创建包含起点终点全航迹 - 计算威胁影响
    XS = [xs, x, xt]
    YS = [ys, y, yt]
    # 设计参数
    k = len(XS)
    #  # 计算航迹段长度，确定时间坐标
    for a in range(k):
        L1 = sqrt((XS[a + 1] - XS[a]) ^ 2 + (YS[a + 1] - YS[a]) ^ 2)
        L = L + L1 
        Tt = ceil(L1 / 0.15) 
        T = T + Tt
        x1 = linspace(XS[a], XS[a + 1], Tt)
        y1 = linspace(YS[a], YS[a + 1], Tt)
        if a == 1:
            xx = x1
            yy = y1
        else:
            xx = [xx, x1]
            yy = [yy, y1]

    nobs =  len(xobs) + 1   # 威胁数量
    ts = 1   # 参数
    #  # 进行威胁影响判断
    for t in range(0, T, 5):
        xd = 0
        yd = 0

        # 威胁集
        xobsd = [xobs, xd]
        yobsd = [yobs, yd]
        robsd = [robs, rd]
        # 判断航迹是否受静态威胁影响
        for k in range(nobs - 1):
            d = sqrt((xx[t] - xobsd[k]) ^ 2 + (yy[t] - yobs[k]) ^ 2)   # 距离
            v = max(1 - d / (robsd[k] + 0.15), 0)   # 判断安全
            Violation = Violation + mean(v)   # 计算平均值
        # 移动威胁预测后分析移动威胁影响
        if t < 50:
            vdt = vdt + dd[ceil(xx[t])][ceil(yy[t])]
            #vdt = vdt + dd {1, ts}(ceil(xx(t)), ceil(yy(t)))
            ts = ts + 1

        #  # 航迹约束
    for i in range(len(xv) - 2):
        a1 = xv[i + 1] - xv[i]
        a2 = yv[i + 1] - yv[i] 
        b1 = xv[i + 2] - xv[i + 1] 
        b2 = yv[i + 2] - yv[i + 1] 
        a = [a1, a2] 
        b = [b1, b2] 

        s1 = rad2deg(atan2(a[0], a[1]))
        s2 = rad2deg(atan2(b[0], b[1]))
        if (s1 - s2) > 75 or (s1 - s2) < -75:
            vs = vs + 1
        #  # 输出航迹数据（坐标时间） 输出航迹代价
        # sol2.TS = TS
    vd = 0
    sol2 :Solution
    sol2.XS = XS
    sol2.YS = YS
    # sol2.tt = tt
    sol2.T = T
    sol2.xx = xx
    sol2.yy = yy
    # sol2.dx = dx
    # sol2.dy = dy
    sol2.L = L
    sol2.Violation = Violation
    sol2.vdt = vdt
    sol2.IsFeasible = (Violation == 0)
    sol2.v = vd
    sol2.vs = vs

