# 这个文件是为了把k_means算法封装起来，形成一个函数，只是分类，不画图
# 函数设计
# 输入：n乘以2的numpy矩阵，分成的类数m
# 返回：m个xxx乘以2的矩阵

# 思考; 如何定初始的中心点，使迭代次数降低


import random
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


# 计算每个两点之间的距离平方
def distance_sq(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    # print(str(x1)+','+str(y1))
    return abs(x1-x2)**2+abs(y1-y2)**2


def apart(point, cen_dict):
    cens = []
    for key in cen_dict.keys():
        cens.append(cen_dict[key][-1])
    point_dict = {}
    num = 0
    for i in cens:
        num += 1
        name = 'center' + str(num)
        point_dict[name] = np.array([False])
    for p in point:
        dt = []
        for cen in cens:
            dt.append(distance_sq(p, cen))
        min_no = min_dt(dt)[0]
        name = 'center' + str(min_no)
        if point_dict[name].all():
            point_dict[name] = np.concatenate([point_dict[name], p])
        else:
            point_dict[name] = p
    for key in point_dict.keys():
        if  point_dict[key].all():
            point_dict[key] = point_dict[key].reshape(-1, 2)
    return point_dict

def min_dt(dt_list):
    num = 0
    min_num = dt_list[0]
    n = 0
    for i in dt_list:
        n += 1
        if i <= min_num:
            min_num = i
            num = n
    return num,min_num


def reset_cen(pdict, cdict):
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


def draw(point_dict,cen_p1,cen_p2):
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

    ax.plot(cen_p1[:, 0], cen_p1[:, 1], '--r', marker=cut_star, markersize=10)  # 画两个中心点轨迹
    ax.plot(cen_p2[:, 0], cen_p2[:, 1], '--r', marker=cut_star, markersize=10, color='b')
    plt.pause(0.1)


def shoulian(cen_dict):
    num = 0
    for cen in cen_dict.keys():
        num += 1
        if cen_dict[cen].shape[0] > 1:
            if cen_dict[cen][-1][0] == cen_dict[cen][-2][0]:
                num -= 1
    return num == 0


def k_means(point, n):
    cen_dict = {}                          # 先定好中心
    for i in range(n):
        name = 'cen_' + str(i+1)                # 先随机吧
        cen_dict[name] = np.array([[random.randint(0, 320), random.randint(0, 320)]])

    for i in range(100):
        if shoulian(cen_dict):
            break
        point_dict = apart(point, cen_dict)  # 按距离分类
        reset_cen(point_dict, cen_dict)  # 重新定中心
    draw(point_dict,cen_dict)

k_means(point,2)
plt.pause(15)