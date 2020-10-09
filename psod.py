from cmath import inf

from numpy import linspace

from CreateModeld import CreateModeld
from CreateRandomSolutiond import CreateRandomSolutiond
from MyCostd import MyCostd
from RRTStar import RRTStar
from gapso import Particle, Best
import numpy as np
#  # 实时规划问题设置

 # ptdx = load('kr.mat', 'ksi_sta_eta_x') 
 # ptdy = load('kr.mat', 'ksi_sta_eta_y') 
 # model.ptdx = ptdx.ksi_sta_eta_x 
 # model.ptdy = ptdy.ksi_sta_eta_y 
model = CreateModeld()   # 环境创建（静态规划，移动中发现移动威胁）
model.n = 5   # 控制点数量

CostFunction = MyCostd   # 代价函数

nVar = model.n   # 决策变量数

VarSize = [1, nVar]   # 决策变量矩阵的大小

VarMin = (model.xmin, model.ymin)   # 变量下限
VarMax = (model.xmax, model.ymax)  # 变量上限


 #  # 粒子群算法参数

MaxIt = 15   # 最大迭代次数

nPop = 150   # 种群数

w = 1   # 惯性因子
wdamp = 0.95   # 迭代惯性因子
c1 = 1.6   # 个体学习因子
c2 = 1.6   # 全体学习因子

alpha = 0.15 
VelMax = (alpha * (VarMax.x - VarMin.x), alpha * (VarMax.y - VarMin.y))    # x y方向最大速度
VelMin = (-VelMax.x, -VelMax.y)   # x y方向最小速度


 #  # 初始化
ep_best = Best(Position=None, Cost=None, Sol=None)
empty_particle = Particle(Position=None, Velocity=None, Cost=None, Sol=None, Best=ep_best)
# 初始化全体最优
GlobalBest = Best(Position=None, Cost=inf, Sol=None)
 # 初始化全体最优

Costbe = inf 

 # particle = repmat(empty_particle, nPop, 1) 
 # 实时规划起点坐标
xst = model.xs 
yst = model.ys 
 # 并行进行粒子存储空间初始化
particle = []
for i in range(nPop):
    particle.append(empty_particle)


 # 实现航迹规划周期循环
while ((10 - xst) ^ 2 + (10 - yst) ^ 2) > 2.25:  # 到达离终点一定距离后停止规划
    model.dd = RRTStar(model)
    model.xs = xst 
    model.ys = yst 
    for i in range(nPop):  # 并行进行粒子初始化
        if i > 1:
            (cx, cy) = CreateRandomSolutiond(model)
            particle[i] = particle[i]._replace(Position=(cx.reshape(-1), cy.reshape(-1)))  # 初始化粒子
        else:
            # 初始化两点间直线
            xx = linspace(xst, model.xt, model.n + 2)
            yy = linspace(yst, model.yt, model.n + 2)
            particle(i).Position.x = xx[1: - 1]
            particle(i).Position.y = yy[1: - 1]


     # 初始化速度
    particle(i).Velocity.x = np.zeros(VarSize)
    particle(i).Velocity.y = np.zeros(VarSize)

     # 航迹代价计算
    [particle(i).Cost, particle(i).Sol] = MyCostd(particle(i).Position, model) 

     # 更新个体最优
    particle(i).Best.Position = particle(i).Position 
    particle(i).Best.Cost = particle(i).Cost 
    particle(i).Best.Sol = particle(i).Sol 

    # 更新集体最优
    for i in range(nPop):
        if particle(i).Best.Cost < GlobalBest.Cost:
            GlobalBest = particle(i).Best
            # 保存最优航迹数据
    BestCost = np.zeros(MaxIt, 1)

    #  # 粒子群迭代循环

    for it in range(MaxIt):  # 迭代次数
        Costbe = GlobalBest.Cost
        for i in range(nPop):  # 种群数
            particle(i).Velocity.x = w * particle(i).Velocity.x + c1 * rand(VarSize). * (particle(i).Best.Position.x - particle(i).Position.x)
    + c2 * rand(VarSize). * (GlobalBest.Position.x - particle(i).Position.x)

            # 更新速度范围
            particle(i).Velocity.x = max(particle(i).Velocity.x, VelMin.x)
            particle(i).Velocity.x = min(particle(i).Velocity.x, VelMax.x)

            # 更新位置
            particle(i).Position.x = particle(i).Position.x + particle(i).Velocity.x

            # 速度镜像
            OutOfTheRange = (particle(i).Position.x < VarMin.x | particle(i).Position.x > VarMax.x)
            particle(i).Velocity.x(OutOfTheRange) = -particle(i).Velocity.x(OutOfTheRange)

            # 更新位置范围
            particle(i).Position.x = max(particle(i).Position.x, VarMin.x)
            particle(i).Position.x = min(particle(i).Position.x, VarMax.x)

            # y轴

            # 更新速度
            particle(i).Velocity.y = w * particle(i).Velocity.y + c1 * rand(VarSize). * (particle(i).Best.Position.y
                             - particle(i).Position.y)+ c2 * rand(VarSize). * (GlobalBest.Position.y - particle(i).Position.y)

            # 更新速度范围
            particle(i).Velocity.y = max(particle(i).Velocity.y, VelMin.y)
            particle(i).Velocity.y = min(particle(i).Velocity.y, VelMax.y)

            # 更新位置
            particle(i).Position.y = particle(i).Position.y + particle(i).Velocity.y

            # 速度镜像
            OutOfTheRange = (particle(i).Position.y < VarMin.y | particle(i).Position.y > VarMax.y)
            particle(i).Velocity.y(OutOfTheRange) = -particle(i).Velocity.y(OutOfTheRange)

            # 更新位置范围
            particle(i).Position.y = max(particle(i).Position.y, VarMin.y)
            particle(i).Position.y = min(particle(i).Position.y, VarMax.y)

            # 代价函数
            [particle(i).Cost, particle(i).Sol] = MyCostd(particle(i).Position, model)

            # 更新全局最佳
            if particle(i).Cost < particle(i).Best.Cost:
                particle(i).Best.Position = particle(i).Position
                particle(i).Best.Cost = particle(i).Cost
                particle(i).Best.Sol = particle(i).Sol

            # 更新全局最佳
            if particle(i).Best.Cost < GlobalBest.Cost:
                GlobalBest = particle(i).Best


 # for i=1:nPop
 #
 # if particle(i).Best.Cost < GlobalBest.Cost
     # GlobalBest = particle(i).Best 
 #
 # end
 # end
 #

 # 更新最优代价
    BestCost[it] = GlobalBest.Cost

w = w * wdamp   # 迭代更新惯性因子

 # Show
Iteration
Information
 # if GlobalBest.Sol.IsFeasible
     # Flag = ' @' 
 # else
 # Flag = [', ' num2str(GlobalBest.Sol.Violation)] 
 # end
    print(['Iteration :{} Best Cost = {} '.format(str(it),str(BestCost(it))) ])

 # PlotSolution
 # figure(1) 
 # PlotSolution(GlobalBest.Sol, model) 
 # pause(0.01) 
 # 迭代收敛，连续多次最优变化极小停止迭代
    if (Costbe - GlobalBest.Cost) < 0.001 and it > 10:
        break
 # 记录存储航迹数据
xsl = GlobalBest.Sol.xx 
ysl = GlobalBest.Sol.yy 

xst = xsl(11) 
yst = ysl(11) 
XI = xsl(1: 1, 1: 10) 
YI = ysl(1: 1, 1: 10) 
model.x1 = [model.x1 XI] 
model.y1 = [model.y1 YI] 
model.t1 = model.t1 + 10 
GlobalBest.Cost = inf 
end
 #  # 结果

figure 
plot(BestCost, 'LineWidth', 2) 
xlabel('Iteration') 
ylabel('Best Cost') 
grid
on 
 # 绘图

figure(3) 
ls = PlotSolutiond(GlobalBest.Sol, model) 



