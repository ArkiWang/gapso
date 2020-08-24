from cmath import sqrt
from collections import namedtuple
from math import ceil, atan2

from numpy import linspace, rad2deg
import copy

from CreateModel import Model
Solution = namedtuple("Solution", "T XS YS xx yy L Violation vdt IsFeasible v vs")

def ParseSolution(sol1, model:Model) ->Solution:
    # 输入航迹数据，环境数据
    (xb, yb) = sol1
    x = [xbb for xbb in xb]

    y = [ybb for ybb in yb]
    dt = model.dt 
    xs = model.xs 
    ys = model.ys 
    xt = model.xt 
    yt = model.yt 
    xobs = model.xobs 
    yobs = model.yobs 
    robs = model.robs

    #创建航迹空间参数
    vs = 0
    vd = 0
    dty = dt
    Violation = 0
    vdt = 0
    # 创建起点与航迹节点集 - 进行角度计算
    xv = [xs]+x
    yv = [ys]+y
    # 创建包含起点终点全航迹 - 计算威胁影响
    XS = [xs]+x+[xt]
    YS = [ys]+y+[yt]
    # 设置参数
    k = len(XS)
    T = 0
    L = 0

    xx = []
    yy = []


    # 计算航迹段长度，确定时间坐标
    for ki in range(k-1):
        L1 = sqrt((XS[ki + 1] - XS[ki])**2 + (YS[ki + 1] - YS[ki])**2)
        L = L + L1
        Tt = ceil(L1.real / 0.15)
        T = T + Tt
        x1 = linspace(XS[ki], XS[ki + 1], Tt)
        y1 = linspace(YS[ki], YS[ki + 1], Tt)
        x1 = list(x1)
        y1 = list(y1)
        if ki == 0:
            xx = copy.deepcopy(x1)
            yy = copy.deepcopy(y1)
        else:
            xx = xx + x1
            yy = yy + y1

    nobs = len(xobs)  # 威胁数量

    # 判断航迹是否受静态威胁影响
    for t in range(T):
        for k in range(nobs):
            d = sqrt((xx[t] - xobs[k])**2 + (yy[t] - yobs[k])**2)  # 距离
            v = max(1 - d.real / (robs[k] + 0.3), 0)  # 判断安全
            Violation = Violation + v  # 计算平均值
            vd = vd + d
        if xx[t] > 0 and yy[t] > 0:
            vdt = vdt + dty[ceil(xx[t])-1][ceil(yy[t])-1]  # 动态威胁预测
    vd = 0
    # 航迹约束
    for i in range(len(x)-1):
        a1 = xv[i + 1] - xv[i]
        a2 = yv[i + 1] - yv[i]
        b1 = xv[i + 2] - xv[i + 1]
        b2 = yv[i + 2] - yv[i + 1]
        a = [a1, a2]
        b = [b1, b2]
        s1 = rad2deg(atan2(a[0], a[1]))
        s2 = rad2deg(atan2(b[0], b[1]))
        if (s1 - s2) > 90 or (s1 - s2) < -90:
            vs = vs + 1

    # 输出航迹数据（坐标时间） 输出航迹代价

    return Solution(T=T, XS=XS, YS=YS, xx=xx, yy=yy, L=L, Violation=Violation, vdt=vdt, IsFeasible=(Violation==0), v=vd, vs=vs)







