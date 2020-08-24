import json
import numpy as np
import matplotlib.pyplot as plt
def load_state(filename):
    states = []
    with open(filename, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        for d in json_data:
            states.append(d)

    return states

def static_p(dis):
    r_max = 80000
    r_min = 50000
    if dis>=r_max:
        return 0
    elif  r_min<dis<r_max:
        return (r_max**4)/(dis**4 +r_max**4)
    else:
        return 1

def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)*(x2-x1) +(y2-y1)*(y2-y1))
def map_to_grid(point,grid_num):
    x_corride = []
    y_corride = []
    step = int(350000/grid_num)
    for i in range(-175000,176000,step):
        x_corride.append(i)
    for j in range(175000,-176000,-step):
        y_corride.append(j)
    m = 0
    n = 0
    for i in x_corride:
       if point[0]<i:
           break
       m += 1
    for j in y_corride:
       if point[1]>j:
            break
       n += 1
    return n,m


def map_2_center_corride(grid_num):
    x_corride = []
    y_corride = []
    step = int(350000/grid_num)
    for i in range(-175000, 176000, step):
        x_corride.append(i)
    for j in range(175000, -176000, -step):
        y_corride.append(j)

    map_center_point = []

    for i in range(1,len(y_corride)):
        row_map_point = []
        y_center = (y_corride[i-1] + y_corride[i])/2
        for j in range(1,len(x_corride)):
             x_center = (x_corride[j-1] + x_corride[j])/2
             row_map_point.append((x_center,y_center))
        map_center_point.append(row_map_point)

    return map_center_point

class bomber:
    def __init__(self,qb):
        #敌方歼击机单元
        self.enemy_a2a_unit = []
        #敌方预警机单元
        self.enemy_awscs_unit = []
        #敌方地面防空单元
        self.enemy_grounndDefine_unit = []
        #敌方护卫舰单元
        self.enemy_ship_unit = []
        #敌方雷达单元
        self.enemy_radar_unit = []
        #歼击机威胁值
        self.a2a_threat_value = 5
        #预警机威胁值
        self.awscs_threat_value = 1
        #护卫舰威胁值
        self.ship_threat_value = 5
        #地面防空威胁值
        self.groundDefine_threat_value = 5
        #雷达威胁值
        self.radar_threat_value = 1

        for unit in qb:
            if unit['LX'] == 11:
                self.enemy_a2a_unit.append(unit)
            elif unit['LX'] == 12:
                self.enemy_awscs_unit.append(unit)
            elif unit['LX'] == 21:
                self.enemy_ship_unit.append(unit)
            elif unit['LX'] == 31:
                self.enemy_grounndDefine_unit.append(unit)
            elif unit['LX'] == 32:
                self.enemy_radar_unit.append(unit)

    def calculate_threat_matrix(self,grid_num):
        threat_matrix = np.zeros((grid_num, grid_num))
        threat_matrix = self.calculate_a2a_threat_matrix(grid_num) +self.calculate_ship_threat_matrix(grid_num)
        return threat_matrix

    def calculate_a2a_threat_matrix(self,grid_num):
        maxtrix_a2a = np.zeros((grid_num, grid_num))
        map = map_2_center_corride(grid_num)
        # 歼击机威胁值计算
        for unit in self.enemy_a2a_unit:
            if unit['WH'] == 1:
                x = unit['X']
                y = unit['Y']
                damage = unit['DA']
                d = unit['HX']
                v = unit['SP']
                # 按100秒预测
                next_pos = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
                pre_pos = [-10, -20, -30, -40, -50, -60, 70, -80, -90, -100]
                pre_cell = []
                next_cell = []
                for i in next_pos:
                    next_pos_y = y + v * np.cos(d) * i
                    next_pos_x = x + v * np.sin(d) * i
                    m, n = map_to_grid((next_pos_x, next_pos_y), grid_num)
                    if (m, n) not in next_cell:
                        next_cell.append((m, n))

                for j in pre_pos:
                    next_pos_y = y + v * np.cos(d) * j
                    next_pos_x = x + v * np.sin(d) * j
                    m, n = map_to_grid((next_pos_x, next_pos_y), 100)
                    if (m, n) not in pre_cell:
                        pre_cell.append((m, n))

                for i in range(len(map)):
                    for j in range(len(map[0])):
                        center_x, center_y = map[i][j]
                        dis = distance(x, y, center_x, center_y)
                        # 静态概率计算
                        p = static_p(dis)
                        value = self.a2a_threat_value * p * (100 - damage) / 100
                        maxtrix_a2a[i][j] += value

                # 航向之前，更危险
                for cell in next_cell:
                    # 边界检测
                    if 1 < cell[0] < len(map) and 1 < cell[1] < len(map[0]):
                        next_x,next_y= map[cell[0]][cell[1]]
                        for i in range(len(map)):
                            for j in range(len(map[0])):
                                center_x,center_y = map[i][j]
                                dis = distance(next_x,next_y,center_x,center_y)
                                p = static_p(dis)
                                value = self.a2a_threat_value * p * (100-damage)/100
                                value = value*1.1
                                maxtrix_a2a[i][j] += value
                for cell in pre_cell:
                    if 1 < cell[0] < len(map) and 1 < cell[1] < len(map[0]):
                        pre_x,pre_y = map[cell[0]][cell[1]]
                        for i in range(len(map)):
                            for j in range(len(map[0])):
                                center_x,center_y = map[i][j]
                                dis = distance(pre_x,pre_y,center_x,center_y)
                                p = static_p(dis)
                                value = self.a2a_threat_value * p * (100-damage)/100
                                value = value*0.8
                                maxtrix_a2a[i][j] += value
        return maxtrix_a2a

    def calculate_ship_threat_matrix(self,grid_num):
        maxtrix_ship = np.zeros((grid_num, grid_num))
        map = map_2_center_corride(grid_num)
        # 护卫舰威胁值计算
        for unit in self.enemy_ship_unit:
            if unit['WH'] == 1:
                x = unit['X']
                y = unit['Y']
                damage = unit['DA']
                d = unit['HX']
                v = unit['SP']
                for i in range(len(map)):
                    for j in range(len(map[0])):
                        center_x, center_y = map[i][j]
                        dis = distance(x, y, center_x, center_y)
                        # 静态概率计算
                        p = static_p(dis)
                        value = self.ship_threat_value * p * (100 - damage) / 100
                        maxtrix_ship[i][j] += value


        return maxtrix_ship


    def Visualization_heatmap(self,matrix):
        def f(x,y):
            return maxtrix[x][y]


        fig = plt.figure()  # 定义新的三维坐标轴
        ax3 = plt.axes(projection='3d')

        # 定义三维数据
        m = np.size(maxtrix,0)
        n = np.size(maxtrix,1)

        xx = np.arange(0, n, 1)
        yy = np.arange(0, m, 1)
        X, Y = np.meshgrid(xx, yy)
        Z = f(X,Y)


        # 作图
        ax3.plot_surface(X, Y, Z[0][0], cmap='rainbow')
        # ax3.contour(X,Y,Z, zdim='z',offset=-2，cmap='rainbow)   #等高线图，要设置offset，为Z的最小值
        plt.show()























if __name__ == "__main__":
    states = load_state('state.json')
    for state_index in range(0, len(states)):
        qb = states[state_index]['red']['qb']
        bomber_agent = bomber(qb)
        maxtrix = bomber_agent.calculate_threat_matrix(grid_num=100)
        bomber_agent.Visualization_heatmap(maxtrix)

















