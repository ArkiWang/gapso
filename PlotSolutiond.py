from numpy import linspace, pi


def PlotSolutiond(sol, model):
    # 绘制最终航迹规划图
    # 输入航迹数据 环境数据
    # xs = model.xs
    # ys = model.ys
    t0 = model.t0
    t1 = model.t1
    xt = model.xt
    yt = model.yt
    x0 = model.x0
    y0 = model.y0
    xobs = model.xobs
    yobs = model.yobs
    robs = model.robs
    rd = model.rd
    ptdx = model.ptdx
    ptdy = model.ptdy
    x1 = model.x1
    y1 = model.y1
    XS = sol.XS
    YS = sol.YS
    xx = sol.xx
    yy = sol.yy
    T = sol.T
    theta = linspace(0, 2 * pi, 100)

    a = 'ture'
    # 颜色
    aa :list
    aa[0] = [1, 0, 0]
    aa[1] = [1, 0, 0]
    aa[2] = [0, 1, 0]
    aa[3] = [0, 1, 0]
    aa[4] = [0, 0, 1]
    aa[5] = [0, 0, 1]
    # plot(XS, YS, 'ro')
    # 静态威胁绘制
    for k in range(len(xobs)):
        fill(xobs(k) + robs(k) * cos(theta), yobs(k) + robs(k) * sin(theta), aa{1, k})


        plot(0.5, 0.5, 'bs', 'MarkerSize', 12, 'MarkerFaceColor', 'y') # 起飞位置
plot(xt, yt, 'kp', 'MarkerSize', 16, 'MarkerFaceColor', 'g') # 实时重规划起点
# 移动威胁位置
xd = [10]
yd = [0]
# rd = [0.75]
p = fill(xd + rd * cos(theta), yd + rd * sin(theta), [0 0 0])
plot(x0, y0, '--b', 'LineWidth', 2)
# if (t > 10)
    # 实时飞行绘制
    for t=1:t1
    # 移动威胁位置
    if (t + t1 <= 10) & & (t + t1 > 292 & & t + t2 < 312)
        xd = 10
    yd = 0
    elseif(t <= 151 & & t > 10)
    xd = ptdx(t - 10)
    yd = ptdy(t - 10)
    elseif((151 <= t) & & (t < 292))
    xd = ptdx(292 - t)
    yd = ptdy(292 - t)
    elseif((t > 313) & & (t < 423))
    xd = ptdx(t - 312)
    yd = ptdx(t - 312)
    elseif(t >= 423)

    end
    set(p, 'XData', xd + rd * cos(theta), 'YData', yd + rd * sin(theta)) # 绘制移动威胁
# for k=1:numel(xd)
# fill(xd(k) + rd(k) * cos(theta), yd(k) + rd(k) * sin(theta), [0 0 0])
# end
if t <= t0
    plot(x0(t), y0(t), 'o') # 静态航迹段

# fid = fopen('E:\data.txt', 'a')
# fprintf(fid, '#d,', t, 1, x0(t), y0(t), 20)
# fprintf(fid, '#s \n,', a)
# 数据类型为整数，中间以逗号分隔
# fclose(fid)

end
if (t0 < t) & & (t <= t1)
    plot(x1(t - t0 + 1), y1(t - t0 + 1), 'o') # 实时重规划航迹段
# l = l + 0.15 * sqrt((x1(t - t0 + 1) - x1(t - t0)) ^ 2 + (y1(t - t0 + 1) - y1(t - t0)) ^ 2)
# fid = fopen('E:\data.txt', 'a')
# fprintf(fid, '#d,', t, 1, x1(t - t0), y1(t - t0), 20)
# fprintf(fid, '#s \n,', a)
# 数据类型为整数，中间以逗号分隔
# fclose(fid)
end
if (t == t1) # 距离终点一定距离最后一段直线航迹
    plot([x1(t - t0), xt], [y1(t - t0), yt])

end

# 地图大小
xlim([0 12])
ylim([0 12])
# 坐标轴
set(gca, 'xtick', 0: 1:12)
set(gca, 'ytick', 0: 1:12)
# 注释
legend('雷达1', '雷达2', '防空武器1', '防空武器2', '干扰设备1', '干扰设备2', '起点', '终点', '移动威胁', '静态航迹轨迹', '实时航迹点', 'Location',
       'southeastoutside')

# gif绘制方法
frame = getframe(gcf)
imind = frame2im(frame)
[imind, cm] = rgb2ind(imind, 256)
if t == 1
    imwrite(imind, cm, 'test.gif', 'gif', 'Loopcount', inf, 'DelayTime', 1e-4)
else
    imwrite(imind, cm, 'test.gif', 'gif', 'WriteMode', 'append', 'DelayTime', 1e-4)
end
end

# ls = l # 输出长度
hold
off
grid
off
axis
equal
l = 0
for t =1:t1
if t < t0
    l = l + sqrt((x0(t + 1) - x0(t)) ^ 2 + (y0(t + 1) - y0(t)) ^ 2)
end
if (t0 < t) & & (t <= t1)
    l = l + sqrt((x1(t - t0 + 1) - x1(t - t0)) ^ 2 + (y1(t - t0 + 1) - y1(t - t0)) ^ 2)
end
if (t == t1) # 距离终点一定距离最后一段直线航迹
    l = l + sqrt((xt - x1(t - t0 + 1)) ^ 2 + (yt - y1(t - t0 + 1)) ^ 2)
end
end
ls = l # 输出长度
end