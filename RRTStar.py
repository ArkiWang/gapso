from math import pi


def RRTStar(model):
    #输入移动威胁数据
    ptdx = model.ptdx 
    ptdy = model.ptdy 
    dt = model.dt   # 输入博弈移动威胁预测概率图
    t0 = model.t0   # 输入时间
 # t = model.t1 
 #
 # a = load('kr.mat', 'ksi_sta_eta_x') 
 # b = load('kr.mat', 'ksi_sta_eta_y') 
 # dt = load('dt.mat', 'dt')   # 输入博弈移动威胁预测概率图
 # model.dt = dt.dt 
 # ptdx = a.ksi_sta_eta_x 
 # ptdy = b.ksi_sta_eta_y 
 # t0 = 10 

 # hold on
 #tic
    # 地图大小
    max.x = 10
    max.y = 10
    bx = [[]]
    by = [[]]
     # 根据时间输入移动威胁位置
    if t0 <= 10and t0 > 292 and t0 < 312:
        pass
     #  xd = 10
    #   yd = 0
    elif t0 <= 151 and t0 > 10:
        bx[0][0] = ptdx(t0 - 10)
        by[0][0] = ptdy(t0 - 10)
        bx[0][1] = ptdx(t0 - 9)
        by[0][1] = ptdy(t0 - 9)
    elif 151 <= t0 and t0 < 292:
        bx[0][0] = ptdx(292 - t0)
        by[0][0] = ptdy(292 - t0)
        bx[0][1] = ptdx(291 - t0)
        by[0][1] = ptdy(291 - t0)
    elif t0 > 313 and t0 < 423:
        bx[0][0] = ptdx(t0 - 312)
        by[0][0] = ptdy(t0 - 312)
        bx[0][1] = ptdx(t0 - 311)
        by[0][1] = ptdy(t0 - 311)
    elif t0 >= 423:
        pass


    # 构建RRT树
    l = [[1], [1]]
    ps = [[1], [1]]
    p = [[1], [1]]
    for a in range (3, 12):
        bx[a] = [] 
        by[a] = [] 
        l[a] = [] 
        ps[a] = [] 
        p[a] = [] 
    # 扩展参数
    ang = [pi / 6, 0, -pi / 6]  # 角度
    pa = [1 / 6, 2 / 3, 1 / 6]   # 概率

    # 进行RRT树的延展
    # while (flag == 1)
    t = 1
    # 确定威胁移动速度的向量 - 计算扩展长度及方向
    vx = bx[0][t] - bx[t - 1][l[0][t]]
    vy = by{1, t} - by{1, t - 1(l{1, t}
    vlong = 5 * sqrt(vx ^ 2 + vy ^ 2)   # 通过XY轴距离确定速度为RRT扩展步长
    for t in range(2, 12):
        # i = i + 1
        pt = 0
        r = size(bx{1, t})   # 读取r
        for i in range(1, r(2))   # 建立for循环嵌套
            vx = bx{1, t}(i) - bx{1, t - 1}(l{1, t}(i))
            vy = by{1, t}(i) - by{1, t - 1}(l{1, t}(i))

vang = atan(vy / vx)   # 确定方向角度
if (p{1, t}(i) > 0.1)  # 筛选节点，排除低概率节点
for j = 1:3  # 扩展3个节点
 # 节点扩展方法
根据不同方向正负角度不同
if (vx < 0 & & vy < 0)
    dotx = bx
    {1, t}(i) + vlong * cos(vang + pi + ang(j)) 
doty = by
{1, t}(i) + vlong * sin(vang + pi + ang(j)) 
elseif(vx > 0 & & vy > 0)
dotx = bx
{1, t}(i) + vlong * cos(vang + ang(j)) 
doty = by
{1, t}(i) + vlong * sin(vang + ang(j)) 
elseif(vx < 0 & & vy > 0)
dotx = bx
{1, t}(i) + vlong * cos(vang + pi + ang(j)) 
doty = by
{1, t}(i) + vlong * sin(vang + pi + ang(j)) 
elseif(vx > 0 & & vy < 0)
dotx = bx
{1, t}(i) + vlong * cos(vang + ang(j)) 
doty = by
{1, t}(i) + vlong * sin(vang + ang(j)) 
end
if (dotx < 10 & & doty < 10 & & dotx > 0 & & doty > 0)
     # plot([bx{1, t}(i), dotx], [by{1, t}(i), doty], 'k', 'LineWidth', 3)   # 绘制扩展节点影响时间，测试使用
pdots = ps
{1, t}(i) * pa(j) * probnode(dotx, doty, model)   # 计算节点概率
 # 扩展节点加入RRT
bx
{1, t + 1} = [bx{1, t + 1}, dotx] 
by
{1, t + 1} = [by{1, t + 1}, doty] 
ps
{1, t + 1} = [ps{1, t + 1}, pdots] 
l
{1, t + 1} = [l{1, t + 1}, i] 
pt = pt + pdots 
end
end

 #  # plot
the
edge
 # xpoints = [qbestNeighb(1, 1), qnew(1, 1)] 
 # ypoints = [qbestNeighb(1, 2), qnew(1, 2)] 
 # hold
on
 # plot(xpoints, ypoints, 'b')
end
end
 # 计算航迹概率
s = size(ps
{1, t + 1}) 
for k = 1:s(2)
pdot = ps
{1, t + 1}(k) / pt 
p
{1, t + 1} = [p{1, t + 1}, pdot] 
end

end
 #  # 进行栅格化
减少运算量
for t = 2:11
dd
{1, t - 1} = [] 
r = size(bx
{1, t})   # 读取r
dl = zeros(max.x, max.y) 
for i = 1:r(2)
dl(ceil(bx
{1, t}(i)), ceil(by
{1, t}(i))) = dl(ceil(bx
{1, t}(i)), ceil(by
{1, t}(i)))+0.5 * p
{1, t}(i) 
dl(ceil(bx
{1, t}(i))+1, ceil(by
{1, t}(i))) = dl(ceil(bx
{1, t}(i))+1, ceil(by
{1, t}(i)))+0.125 * p
{1, t}(i) 
dl(ceil(bx
{1, t}(i)), ceil(by
{1, t}(i))+1) = dl(ceil(bx
{1, t}(i)), ceil(by
{1, t}(i))+1)+0.125 * p
{1, t}(i) 
dl(ceil(bx
{1, t}(i))-1, ceil(by
{1, t}(i))) = dl(ceil(bx
{1, t}(i))-1, ceil(by
{1, t}(i)))+0.125 * p
{1, t}(i) 
dl(ceil(bx
{1, t}(i)), ceil(by
{1, t}(i))-1) = dl(ceil(bx
{1, t}(i)), ceil(by
{1, t}(i))-1)+0.125 * p
{1, t}(i) 
end
dd
{1, t - 1} = [dd{1, t - 1}, dl] 
end
pwt = dd 

toc
end

