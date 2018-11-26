# K-means
初级的K-means算法，简单地分两类
K-means算法基本步骤
(1)给K个cluster选择最初的中心点，称为K个means。（此时的聚类中心依据经验或任意指定）
(2)计算每个对象和每个中心点之间的距离
(3)把每个对象分配给据它最近的中心点做属的cluster
(4)重新计算每个cluster的中心点。（K-means中新的聚类中心，由类中所有点各维的平均值计算得来）
(5)重复2,3,4步，直到算法收敛



本次实验分为3个步骤
1、产生两堆数据，有一定的类别和随机性
2、对这些数据进行K-means算法
3、绘制动态图，将数据可视化
