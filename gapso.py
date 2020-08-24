from collections import namedtuple
from math import inf
import numpy as np
import copy
from numpy import linspace, clip
from CreateRandomSolution import CreateRandomSolution
from CreateModel import CreateModel
from Mycost import MyCost
from PlotSolution import PlotSolution
from crossover import crossover
from mutation import mutation

Particle = namedtuple("Particle", "Position Velocity Cost Sol Best")
Best = namedtuple("Best", "Position Cost Sol")
def getOutTheRange(VarMin_xy: int, VarMax_xy: int, posxy: [])->[]:
    OutOfTheRange = []
    pxl = []
    for p in posxy:
        if p < VarMin_xy:
            pxl.append(1)
        else:
            pxl.append(0)
    pxr = []
    for p in posxy:
        if p > VarMax_xy:
            pxr.append(1)
        else:
            pxr.append(0)
    for i in range(len(pxl)):
        if pxl[i] == 1 or pxr == 1:
            OutOfTheRange.append(1)
        else:
            OutOfTheRange.append(0)
    return OutOfTheRange
def consttimesverctor(times: int,v: []) -> []:
    for i in range(len(v)):
        v[i] *= times
    return v
def vectortimesverctor(v1 :[], v2: []) -> []:
    ans = []
    for i in range(len(v1)):
        ans.append(v1[i]*v2[i])
    return ans
def vectorplusvector(v1 :[], v2: []) -> []:
    ans = []
    for i in range(len(v1)):
        ans.append(v1[i]+v2[i])
    return ans
def updatespeed(w: int, vx: [], c1: int, VarSize: [],bpx_px: [], c2: int, gpx_px: []) -> []:
    a = consttimesverctor(w,vx)
    b = vectortimesverctor(c1 * np.random.rand(VarSize[0], VarSize[1]).reshape(-1),bpx_px)
    c = vectortimesverctor(c2 * np.random.rand(VarSize[0], VarSize[1]).reshape(-1),gpx_px)
    d = vectorplusvector(a, b)
    return  vectorplusvector(d, c)
def gapso() ->None:
    # 静态航迹规划采用遗传 - 粒子群算法

    #  # 问题设置
    model = CreateModel()   # 环境创建
    model = model._replace(n=5) # 控制点数量

    nVar = model.n   # 决策变量数

    VarSize = [1, nVar]   # 决策变量矩阵的大小
    VarMin = (model.xmin, model.ymin)#变量下限
    VarMax = (model.xmax, model.ymax)#变量上限

    #  # 算法参数

    MaxIt = 50   # 最大迭代次数

    nPop = 250   # 种群数

    w = 1   # 惯性因子
    wdamp = 0.98   # 迭代惯性因子
    c1 = 1.5   # 个体学习因子
    c2 = 1.5   # 全体学习因子

    alpha = 0.1
    (vmax_x, vmax_y) = VarMax
    (vmin_x, vmin_y) = VarMin
    VelMax = (alpha * (vmax_x - vmin_x), alpha * (vmax_y - vmin_y))#x,y方向最大速度
    VelMin = (-vmax_x, -vmax_y)#x,y方向最小速度


    #  # 初始化
    # 创建空结构
    ep_best = Best(Position=None, Cost=None, Sol=None)
    empty_particle = Particle(Position=None, Velocity=None, Cost=None, Sol=None, Best=ep_best)
    # 初始化全体最优
    GlobalBest = Best(Position=None, Cost=inf, Sol=None)

    # 染色体存储空间初始化
    #particle = repmat(empty_particle, nPop, 1)
    particle = []
    for i in range(nPop):
        particle.append(empty_particle)

    # 初始化循环
    for i in range(nPop):
        if i > 0:
            (cx, cy) = CreateRandomSolution(model)
            particle[i] = particle[i]._replace(Position = (cx.reshape(-1),cy.reshape(-1)))  # 初始化粒子
        else:
            # 初始化两点间直线
            xx = linspace(model.xs, model.xt, model.n + 2)
            yy = linspace(model.ys, model.yt, model.n + 2)
            particle[i] = particle[i]._replace(Position=(xx[1: -1], yy[1: -1]))


        # 初始化速度
        particle[i] = particle[i]._replace(Velocity = (np.zeros(VarSize).reshape(-1), np.zeros(VarSize).reshape(-1)))
        (x, y) = particle[i].Position

        # 航迹代价计算
        (pic, pis) = MyCost(particle[i].Position, model)
        particle[i] = particle[i]._replace(Cost=pic, Sol=pis)
        #[particle[i].Cost, particle[i].Sol] = MyCost(particle[i].Position, model)

        # 更新个体最优
        particle[i] = particle[i]._replace(Best=Best(Position=particle[i].Position, Cost=particle[i].Cost, Sol=particle[i].Sol))

        # 更新集体最优
        if particle[i].Best.Cost.real < GlobalBest.Cost.real:
            GlobalBest = particle[i].Best



    # 保存最优航迹数据
    BestCost = np.zeros(MaxIt)

    #  # 迭代过程

    for it in range(MaxIt):
    # 交叉变异 - 更新染色体
        for i in range(nPop):
            if i < nPop - it:
                (sol1 ,sol2) = crossover(particle[i].Position, particle[i + it].Position)
                particle[i] = particle[i]._replace(Position = sol1)   # 交叉
                particle[i + it] = particle[i + it]._replace(Position = sol2)
            else:
                (sol1, sol2) = crossover(particle[i] .Position, particle[nPop - it].Position)
                particle[i] = particle[i]._replace(Position = sol1)
                particle[nPop - it] = particle[nPop - it]._replace(Position = sol2)

            particle[i]= particle[i]._replace(Position = mutation(particle[i].Position) )  # 变异


        (VelMin_x, VelMin_y) = VelMin
        (VelMax_x, VelMax_y) = VelMax
        (VarMin_x, VarMin_y) = VarMin
        (VarMax_x, VarMax_y) = VarMax
        (vx, vy) = particle[i].Velocity
        (px, py) = particle[i].Position
        (bpx, bpy) = particle[i].Best.Position
        (gpx, gpy) = GlobalBest.Position
        # 更新速度
        vx = list(vx);vy = list(vy)
        bpx = list(bpx);bpy = list(bpy)

        bpx_px = [bpx[i]-px[i] for i in range(len(bpx))]
        bpy_py = [bpy[i]-py[i] for i in range(len(bpy))]
        gpx_px = [gpx[i]-px[i] for i in range(len(gpx))]
        gpy_py = [gpy[i]-py[i] for i in range(len(gpy))]
        #velx = w * vx + c1 * np.random.rand(VarSize[0],VarSize[1]) * bpx_px + c2 * np.random.rand(VarSize[0],VarSize[1]) * gpx_px

        velx = updatespeed(w, vx, c1, VarSize, bpx_px, c2, gpx_px)
        # 更新速度范围
        print("velx:", velx)

        velx = clip(velx, VelMin_x,None)
        velx = clip(velx, None,VelMax_x)
        print(px)
        print(velx)
        # 更新位置
        posx = px + velx
        print(posx)
        # 速度镜像
        OutOfTheRange = getOutTheRange(VarMin_x, VarMax_x, posx)

        for i in OutOfTheRange:
            velx[i] = -velx[i]
        # 更新位置范围
        posx = clip(posx, VarMin_x, None)
        posx = clip(posx, None, VarMax_x)

        #vely = w * vy + c1 * np.random.rand(VarSize[0],VarSize[1]) * bpy_py + c2 * np.random.rand(VarSize[0],VarSize[1]) * (gpy - py)
        vely = updatespeed(w, vy, c1, VarSize, bpy_py, c2, gpy_py)
        vely = clip(vely, VelMin_y, None)
        vely = clip(vely, None, VelMax_y)
        posy = py + vely
        OutOfTheRange = getOutTheRange(VarMin_y, VarMax_y, posy)
        print("outoftherange: ",OutOfTheRange)
        for i in OutOfTheRange:
            vely[i] = -vely[i]
        posy = clip(posy, VarMin_y, None)
        posy = clip(posy, None, VarMax_y)

        particle[i] = particle[i]._replace(Position=(posx,posy),Velocity=(velx,vely))


        # 代价函数
        (pic, pis) = MyCost(particle[i].Position, model)
        particle[i] = particle[i]._replace(Cost=pic, Sol=pis)
        #[particle[i] .Cost, particle[i] .Sol] = MyCost(particle[i].Position, model)

        # 更新全局最佳
        if particle[i].Cost.real < particle[i].Best.Cost.real:
            particle[i] = particle[i]._replace(Position=particle[i].Position,Cost=particle[i].Cost,Sol=particle[i].Sol)


        # 更新全局最佳
        if particle[i].Best.Cost.real < GlobalBest.Cost.real:
            GlobalBest = particle[i].Best

         # 更新最优代价
        BestCost[it] = GlobalBest.Cost.real

        w = w * wdamp   # 迭代更新惯性因子

        # 显示最优代价
        if GlobalBest.Sol.IsFeasible:
            Flag = ' @'
        else:
            Flag = [', ', GlobalBest.Sol.Violation]

        print('Iteration ',it, ': Best Cost = ', BestCost[it] ,Flag)

        # 静态航迹绘图

        PlotSolution(GlobalBest.Sol, model)


     #  # 结果输出静态航迹及总时间

    # figure
    # plot(BestCost, 'LineWidth', 2)
    # xlabel('Iteration')
    # ylabel('Best Cost')
    # grid on
    """
    xoyo = ()
    xoyo.x0 = GlobalBest.Sol.xx
    xoyo.y0 = GlobalBest.Sol.yy
    xoyo.T0 = GlobalBest.Sol.T
    return xoyo
    """
    return GlobalBest.Sol


gapso()