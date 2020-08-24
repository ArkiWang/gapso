from collections import namedtuple

import scipy.io as io

Model = namedtuple("Model", "Pl Pt Pdt Pv xs ys xt yt xobs yobs robs n xmin xmax ymin ymax dt")
def CreateModel() -> Model:
    dt = io.loadmat('dt.mat')
    #起点
    xs = 0.5
    ys = 0.5
    #目标点
    xt = 10
    yt = 10
    #静态威胁
    xobs = [9,2,5,7,6,3]
    yobs = [6,7,5,2,8,3]
    robs = 1 * [1.5,1.5,1,1,1.2,1.2]# r值修改范围
    #输出参数和变量
    n = 4

    xmin = 0 
    xmax = 10 

    ymin = 0 
    ymax = 10 
    Pl = 0.6 #长度
    Pt = 0.3 #静态威胁代价
    Pdt = 0.0 #航迹性能代价
    Pv = 0.1#移动威胁预测

    return Model(Pl=Pl, Pt=Pt, Pdt=Pdt, Pv=Pv, xs=xs, ys=ys, xt=xt, yt=yt, xobs=xobs,
                  yobs=yobs, robs=robs, n=n, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, dt=dt.get('dt'))
