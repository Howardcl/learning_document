# 1.autoware.universe规划部分源码学习

## 1.1 behavior_path_planner



## 1.2 behavior_velocity_blind_spot_module



Lidar：激光雷达

Radar：毫米波雷达

# 2.AutowareAuto项目简介

缺点：算法和实现功能远少于Apollo项目

优点：基于ROS2和DDS，工具生态较好且实现比较简单。

基于激光点云的感知和匹配定位

==最为人诟病的一点：缺少视觉感知==

针对复杂场景，表现一般。

自动待客泊车AVP在简单场景下能正常工作。

导航：NDT算法

![image-20230810142136836](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308101426180.png)

![image-20230810143024611](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308101430689.png)

![image-20230810144026899](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308101440027.png)

局部路径规划Behavior Planner：其实不会避障，只是遇到障碍物就停下来。

![image-20230810144448000](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308101444106.png)

**控制决策模块：**

![image-20230810144606337](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308101446405.png)

# 3.Autoware.universe软件框架介绍

控制这块：主要是轨迹跟随，接收决策过来的消息，然后进行横纵向控制。

![image-20230811142118255](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308111421361.png)

![image-20230811142604704](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308111426783.png)

![image-20230811143233624](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308111432751.png)

# 4.Autoware的vehicle_interface界面调研





