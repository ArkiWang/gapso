from cmath import inf

from numba import jit, prange

from gapso import Best, Particle


def CreateModeld():
    return None

@jit(nopython=True, parallel=True)
def psod() -> None:
    """

    """
# 实时规划问题设置

# ptdx = load('kr.mat', 'ksi_sta_eta_x')
# ptdy = load('kr.mat', 'ksi_sta_eta_y')
# model.ptdx = ptdx.ksi_sta_eta_x
# model.ptdy = ptdy.ksi_sta_eta_y
model = CreateModeld() # 环境创建（静态规划，移动中发现移动威胁）
model.n = 5 # 控制点数量


nVar = model.n # 决策变量数

VarSize = [1, nVar] # 决策变量矩阵的大小

VarMin = (model.xmin, model.ymin)  # 变量下限
VarMax = (model.xmax, model.xmin) # 变量上限


# # 粒子群算法参数

MaxIt = 15 # 最大迭代次数

nPop = 150 # 种群数

w = 1 # 惯性因子
wdamp = 0.95 # 迭代惯性因子
c1 = 1.6 # 个体学习因子
c2 = 1.6 # 全体学习因子

alpha = 0.15
VelMax = (alpha * (VarMax.x - VarMin.x), alpha * (VarMax.y - VarMin.y))  # 最大速度
VelMin = (-VelMax.x, -VelMax.y) # 最小速度


# # 初始化

# 创建空结构
ep_best = Best(Position=None, Cost=None, Sol=None)
empty_particle = Particle(Position=None, Velocity=None, Cost=None, Sol=None, Best=ep_best)
# 初始化全体最优
GlobalBest = Best(Position=None, Cost=inf, Sol=None)
Costbe = inf

# particle = repmat(empty_particle, nPop, 1)
# 实时规划起点坐标
xst = model.xs
yst = model.ys
# 并行进行粒子存储空间初始化
particle = []
for i in prange(nPop):
    particle.append(empty_particle)







