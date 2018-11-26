import matplotlib.pyplot as plt
import numpy as np
from numpy import random as nr
import matplotlib.path as mpath
from itertools import zip_longest
# 第一步，产生两类随机数据。数据内容有：x,y坐标值
num = 20   # 产生每类20个随机数
ran = 30   # 随机数在在中心30的距离

p1 = nr.normal(100, ran, size=(2, num)).T
p2 = nr.normal(200, ran, size=(2, num)).T
np.set_printoptions(precision=4)    # 显示保留四位有效数字
point = np.concatenate([p1, p2])   # 合并数据


# 第二步，对数据进行K-means算法
#  K-means算法基本步骤
# (1)给K个cluster选择最初的中心点，称为K个means。（此时的聚类中心依据经验或任意指定）
# (2)计算每个对象和每个中心点之间的距离
# (3)把每个对象分配给据它最近的中心点做属的cluster
# (4)重新计算每个cluster的中心点。（K-means中新的聚类中心，由类中所有点各维的平均值计算得来）
# (5)重复2,3,4步，直到算法收敛

# 令中心点为(100,200),(200,100)
init_cen_x1, init_cen_y1 = (100, 200)
init_cen_x2, init_cen_y2 = (200, 100)




# 计算每个两点之间的距离平方
def distance_sq(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    #print(str(x1)+','+str(y1))
    return abs(x1-x2)**2+abs(y1-y2)**2

def apart(point, cen_a, cen_b):
    point_dict['A'] = np.array([False])
    point_dict['B'] = np.array([False])
    for p in point:
        d_a = distance_sq(p, cen_a)
        d_b = distance_sq(p, cen_b)
        if d_a > d_b:
            if point_dict['B'].all():
                point_dict['B'] = np.concatenate([point_dict['B'], p])
            else:
                point_dict['B'] = p
        else:
            if point_dict['A'].all():
                point_dict['A'] = np.concatenate([point_dict['A'], p])
            else:
                point_dict['A'] = p
    point_dict['A'] = point_dict['A'].reshape(-1, 2)
    point_dict['B'] = point_dict['B'].reshape(-1, 2)


def reset_cen(pdict,cenp1,cenp2):
    sum_x1 = 0
    sum_y1 = 0
    sum_x2 = 0
    sum_y2 = 0
    for p1, p2 in zip_longest(pdict['A'], pdict['B'],  fillvalue=[0,0]):
        sum_x1 += p1[0]
        sum_y1 += p1[1]
        sum_x2 += p2[0]
        sum_y2 += p2[1]
    n1 = pdict['A'].shape[0]
    n2 = pdict['B'].shape[0]
    cen1 = np.array([[sum_x1 / n1, sum_y1 / n1]])
    cen2 = np.array([[sum_x2 / n2, sum_y2 / n2]])
    cenp1 = np.concatenate([cenp1, cen1])
    cenp2 = np.concatenate([cenp2, cen2])
    return cenp1, cenp2


def draw():
    # 以下是画散点图
    plt.ion()  # 交互模式
    fig, ax = plt.subplots()
    ax.plot(point_dict['A'][:, 0], point_dict['A'][:, 1], 'ro', color='m')  # 画随机的散点
    ax.plot(point_dict['B'][:, 0], point_dict['B'][:, 1], 'ro', color='c')
    ax.set_title('K-means')
    plt.pause(0.1)

    star = mpath.Path.unit_regular_star(6)  # 画出中心点的轨迹
    circle = mpath.Path.unit_circle()
    # concatenate the circle with an internal cutout of the star
    verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star = mpath.Path(verts, codes)

    point = ax.plot(cen_p1[:, 0], cen_p1[:, 1], '--r', marker=cut_star, markersize=10)  # 画两个中心点轨迹
    point2 = ax.plot(cen_p2[:, 0], cen_p2[:, 1], '--r', marker=cut_star, markersize=10, color='b')
    plt.pause(0.1)


# 创建中心点坐标数组
cen_p1 = np.array([[init_cen_x1, init_cen_y1]])
cen_p2 = np.array([[init_cen_x2, init_cen_y2]])
# 创建字典，用于存放两类数据
point_dict = {'A': None, 'B': None}
for i in range(10):
    if cen_p1.shape[0] > 1 and cen_p2.shape[0] > 1:     # 中心点不变跳出循环
       if cen_p1[-1][0] == cen_p1[-2][0] and cen_p1[-1][1] == cen_p1[-2][1]:
           if cen_p2[-1][0] == cen_p2[-2][0] and cen_p2[-1][1] == cen_p2[-2][1]:
                break
    apart(point, cen_p1[-1], cen_p2[-1])    # 按距离分类
    cen_p1, cen_p2 = reset_cen(point_dict, cen_p1, cen_p2)   # 重新定中心
    draw()

plt.pause(15)