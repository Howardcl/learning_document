# 1.概述与课程介绍

IMU：零偏

![image-20211025094525497](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025094525497.png)

典型的IMU测量角速度与加速度。

![image-20211025102310152](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025102310152.png)

![image-20211025105319671](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025105319671.png)

![image-20211025110152972](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025110152972.png)

IMU本身的加速度计是有尺度的，不像单目视觉没有尺度。VO静止的时候是不产生漂移的。

![image-20211025140544842](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025140544842.png)

![image-20211025141137870](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025141137870.png)

![image-20211025141513687](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025141513687.png)

松耦合是指视觉和IMU分别进行自身的状态估计，然后对其位姿估计结果进行融合。**就是说这个融合的过程对二者本身的状态估计是不产生影响的。**

**紧耦合是指把IMU的状态和相机的状态合并在一起，共同构建运动方程和观测方程。**

![image-20211025141549228](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025141549228.png)



![image-20211025141607888](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025141607888.png)

![image-20211025141640871](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025141640871.png)

![image-20211025141650409](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025141650409.png)

**齐次坐标：将一个原本是n维的向量用一个n+1维向量来表示。**

![image-20211025161203159](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025161203159.png)

![image-20211025161211589](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025161211589.png)

![image-20211025161907964](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025161907964.png)

![image-20211025161917276](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025161917276.png)

![image-20211025162721494](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025162721494.png)

![image-20211025162753558](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025162753558.png)

![image-20211025163720756](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025163720756.png)

![image-20211025184549354](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025184549354.png)

# 2.IMU传感器

## 2.1 旋转运动学

**在旋转坐标系下观察,运动的物体(运动方向和旋转轴不为同一个轴时)会受到科氏力的作用。 **

![image-20211103172600918](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103172600918.png)

![image-20211103172649598](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103172649598.png)

![image-20211103172702184](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103172702184.png)

## 2.2 IMU测量模型及运动模型

加速度计测的是弹簧拉力所引起的加速度。实际测量量不一定是力，也可能是电容变化引起的电压量变换。

![image-20211103101502047](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103101502047.png)

![image-20211103102314397](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103102314397.png)

![image-20211103102458888](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103102458888.png)

![image-20211103104530422](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103104530422.png)

## 2.3 IMU误差模型

### 2.3.1 IMU确定性误差

确定性误差主要包括bias(偏置)、scale(尺度)、**misalignment(坐标轴互相不垂直)**等多种。常使用六面静置法标定加速度计和陀螺仪的确定性误差。

**==确定性误差：可以事先标定。==**

![image-20211103105051138](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103105051138.png)

![image-20211103105501289](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103105501289.png)

非对齐误差：

矩阵对角线表示Scale误差，非对角就是Misalignment误差

![image-20211103110401294](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103110401294.png)

![image-20211103110515838](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103110515838.png)

很多情况下，确定性误差都是可以标定出来的。

![image-20211103111344196](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103111344196.png)

![image-20211103140730061](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103140730061.png)

陀螺仪的标定法:六面法

![image-20211103140749860](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103140749860.png)

**温度相关的参数标定**

![image-20211103141510752](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103141510752.png)

### 2.3.2 IMU随机误差

IMU随机误差包括高斯白噪声和bias随机游走。

![image-20211103141059397](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103141059397.png)



![image-20211103142752392](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103142752392.png)

![image-20211103142811664](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103142811664.png)

![image-20211103142917628](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211103142917628.png)

**==IMU随机误差的标定==**

![image-20211106161054411](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211106161054411.png)

![image-20211106161123899](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211106161123899.png)

## 2.4 运动模型离散时间处理



### 2.4.1 欧拉法

### 2.4.2 中值法

## 2.5 IMU数据仿真



# 3.基于优化的IMU预积分与视觉信息融合

## 3.1.基于Bundle Adjustment的VIO融合

![image-20211108112014285](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108112014285.png)

b1：body坐标系。

这个VIO信息融合问题。比如说：Camera的频率是30hz，IMU的频率是200HZ，那么在两帧图像之间会产生很多IMU数据，会有将很多IMU的数据进行积分，将其变成一个数据的操作。

![image-20211108112221631](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108112221631.png)

## 3.2 最小二乘问题的求解

**最小二乘基础概念**

![image-20211108112753153](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108112753153.png)

下面描述的是H矩阵的性质；

![image-20211108113109356](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108113109356.png)

求解法：

1.直接求解：线性最小二乘

2.迭代下降法：适用于线性和非线性最小二乘。

### 3.2.1 基础：最速下降法，牛顿法

![image-20211108141719357](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108141719357.png)

![image-20211108141703951](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108141703951.png)

**阻尼法Damp Method**：阻尼是加到H矩阵上面的。

![image-20211108142046747](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108142046747.png)

![image-20211108142226494](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108142226494.png)

==**上面的最速下降法和牛顿法在实际当中都不常用，最速下降法收敛慢，牛顿法H矩阵难求，在实际中都会用它们的改进方法。**==

### 3.2.2 进阶：高斯牛顿法，LM算法的具体实现

高斯牛顿法针对是残差函数$f(x)$，是没平方之前的，之前的是平方之后的$F(x)$。

![image-20211108143402657](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108143402657.png)

![image-20211108143543817](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108143543817.png)

![image-20211108144303231](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108144303231.png)

### 3.2.3 终极：鲁棒核函数

outlier：不小心弄错了残差函数。由于F(x)是平方项，会导致其增长的很快。鲁棒核函数就是处理误匹配

![image-20211108150312037](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108150312037.png)

![image-20211108152042547](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108152042547.png)

==**回顾最小二乘求解**==

![image-20211108152012466](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108152012466.png)

## 3.3 VIO残差函数的构建

VIO是一个基于滑动窗口的Bundle Adjustment。先验误差Prior

![image-20211108152315706](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108152315706.png)

![image-20211108152939021](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108152939021.png)

### 3.3.1 视觉重投影误差

![image-20211108152949127](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108152949127.png)

### 3.3.2 预积分模型由来及意义

![image-20211108191555391](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108191555391.png)

![image-20211108192117608](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108192117608.png)

==**上面就是对IMU的直接积分，但是我们一般不做直接积分。原因就是每次$q_{wb_t}$优化更新后，所有的量都要重新进行积分，运算量较大。**==

==**预积分：将跟世界坐标系有关的量全部抽出来，预积分的积分项变为相对于第i时刻的姿态。**==

![image-20211108193020771](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108193020771.png)

![image-20211108193324988](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108193324988.png)

有了预积分量之后，就可以来做两个状态量之间的误差。

![image-20211108194443851](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108194443851.png)

![image-20211108195727339](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108195727339.png)

### 3.3.3 预积分量方差的计算

![image-20211108195436917](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108195436917.png)

## 3.4 残差Jacobian的推导

### 3.4.1 视觉重投影残差的Jacobian

**这里是整个系统的残差对状态量之间的Jacobian**

![image-20211108203234681](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108203234681.png)

![image-20211108203257572](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211108203257572.png)

### 3.4.2 IMU预积分残差的Jacobian

![image-20211109085102969](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109085102969.png)

# 4.滑动窗口算法理论：VIO融合及其可观性与一致性

## 4.1 从高斯分布到信息矩阵

### 4.1.1 SLAM和高斯分布

![image-20211109111853816](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109111853816.png)

### 4.1.2 从两个例子窥探协方差和信息矩阵

==协方差矩阵的逆，**即信息矩阵**==



## 4.2 舒二补应用：边际概率，条件概率

### 4.2.1 舒尔补

**舒尔补的概念**

![image-20211109150843715](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109150843715.png)

![image-20211109151454395](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109151454395.png)

**使用舒尔补的好处：快速求解矩阵M的逆**

![image-20211109151553135](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109151553135.png)

### 4.2.2 舒尔补与条件概率和边际概率

![image-20211109152545569](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109152545569.png)

### 4.2.3 总结

![image-20211109153010911](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109153010911.png)

## 4.3 滑动窗口算法

### 4.3.1 marg 基础

在我们这个工科领域，它来源于概率论中的边际分布（[marginal distribution](https://en.wikipedia.org/wiki/Marginal_distribution)）。如从联合分布p(x,y)去掉y得到p(x)，也就是说从一系列随机变量的分布中获得这些变量子集的概率分布。回忆了这个概率论中的概念以后，让我们转到SLAM的Bundle Adjustment上，随着时间的推移，路标特征点(landmark)和相机的位姿pose越来越多，BA的计算量随着变量的增加而增加，即使BA的H矩阵是稀疏的，也吃不消。因此，我们要限制优化变量的多少，不能只一味的增加待优化的变量到BA里，而应该去掉一些变量。那么如何丢变量就成了一个很重要的问题！比如有frame1,frame2,frame3 以及这些frame上的特征点pt1…ptn。新来了一个frame4，为了不再增加BA时的变量，出现在脑海里的直接做法是把frame1以及相关特征点pt直接丢弃，只优化frame2,frame3,frame4及相应特征点。然而，这种做法好吗？

Gabe Sibley [2]在他们的论文中就明确的说明了这个问题。**直接丢掉变量，就导致损失了信息**，frame1可能能更多的约束相邻的frame，直接丢掉的方式就破坏了这些约束。在SLAM中，一般概率模型都是建模成高斯分布，如相机的位姿都是一个高斯分布，轨迹和特征点形成了一个多元高斯分布p(x1,x2,x3,pt1…)，然后图优化或者BA就从一个概率问题变成一个最小二乘问题。因此，从这个多元高斯分布中去掉一个变量的正确做法是把他从这个多元高斯分布中marginalize out. 

这marginalize out具体该如何操作呢？Sliding widow Filter [2]中只是简单的一句应用Schur complement（舒尔补）. 我们知道SLAM中的图优化和BA都是最小二乘问题，如下图所示(ref.[1])

![image-20211110153423091](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110153423091.png)

pose graph和BA中，误差函数e是非线性的，这个非线性最小二乘问题可以通过高斯牛顿迭代求得，即H δ x = b .其中$H=J^TWJ,b=JWe$,J是误差对位姿等的雅克比，W是权重。一般这个H矩阵也称为信息矩阵，并且H矩阵是稀疏的，这些都是SLAM中的基础知识。

要求解这个线性方程，可以用QR分解什么的，但是这里我们关注marginalize. 也就是说只去求解我们希望保留的变量，那些我们要marg的变量就不关心了，从而达到减少计算的目的。假设变量x中可以分为保留部分和marg部分，那么上面的线性方程可以写成如下形式：

![image-20211110153546553](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110153546553.png)

这里我们要marg掉$x_a$，而计算$x_b$ , 对上面这个方程进行消元得到：

![image-20211110153603031](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110153603031.png)

![image-20211110153608165](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110153608165.png)

这样我们就能够迭代的更新部分变量，从而维持计算量不增加。在上面这个过程中，我们要注意，构建出来的Hx=b是利用了marg变量的信息，也就是说我们没有人为的丢弃约束，所以不会丢失信息，但是计算结果的时候，我们只去更新了我们希望保留的那些变量的值。在slam的过程中，BA不断地加入新的待优化的变量，并marg旧的变量，从而使得计算量维持在一定水平。这就是sliding window filter, okvis, dso这些论文中marg的应用。

**在整个SLAM问题中，前面的关于协方差、信息矩阵、边界概率、舒尔补都是为了滑动窗口服务的。**

### 4.3.2 图优化基础

![image-20211109152847974](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109152847974.png)

![image-20211109155442973](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109155442973.png)

![image-20211109155820797](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109155820797.png)

![image-20211109162158267](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109162158267.png)

![image-20211109155846960](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109155846960.png)

### 4.3.3 基于边际概率的滑动窗口算法

**为什么要进行边缘化操作？**
首先我们知道，如果仅仅从前后两帧图像来计算相机变换位姿， 其速度快但是精度低，而如果采用全局优化的方法（比如Bundle Adjustment），其精度高但是效率低，因此前辈们引入了滑窗法这样一个方法，每次对固定数量的帧进行优化操作，这样既保证了精度又保证了效率。既然是滑窗，在滑动的过程中必然会有新的图像帧进来以及旧的图像帧离开，所谓边缘化就是为了使得离开的图像帧得到很好的利用。

![image-20211109163933081](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109163933081.png)

![image-20211109164449653](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109164449653.png)

## 4.4 滑动窗口中的FEJ算法

### 4.4.1 滑动窗口算法的系统回顾及深入剖析

![image-20211109165443330](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109165443330.png)

![image-20211109182010450](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109182010450.png)

![image-20211109185748622](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109185748622.png)

### 4.4.2 系统可观性

![image-20211109190318288](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109190318288.png)

![image-20211109191338907](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109191338907.png)

### 4.4.3 滑动窗口算法中存在的问题以及FEJ算法

![image-20211109191348894](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211109191348894.png)

# 5.后端优化实践：逐行手写求解器

## 5.1 非线性最小二乘求解

### 5.1.1 solver流程回顾

构建残差函数，比如视觉SLAM中就是重投影误差。(将像素坐标(观测到的投影位置)与 3D 点按照当前估计的位姿进行投影得到的位置相比较得到的误差,所以称之为重投影误差。)

IMU是预积分误差：IMU动力模型，误差模型。

![image-20211110092431440](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110092431440.png)

![image-20211110095116616](/home/cl/.config/Typora/typora-user-images/image-20211110095116616.png)

![image-20211110095742855](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110095742855.png)

H不满秩，导致求逆会有问题。

![image-20211110095621929](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110095621929.png)

### 5.1.2 solver代码讲解

![image-20211110102537487](/home/cl/.config/Typora/typora-user-images/image-20211110102537487.png)

## 5.2 滑动窗口算法

### 5.2.1 滑动窗口算法回顾

![image-20211110112400970](/home/cl/.config/Typora/typora-user-images/image-20211110112400970.png)

![image-20211110164259607](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110164259607.png)

![image-20211110165255381](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110165255381.png)

### 5.2.2 VINS-Mono中的滑动窗口算法

![image-20211110165711862](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110165711862.png)

# 6.视觉前端

## 6.1 前端的工作

![image-20211110181550657](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110181550657.png)



![image-20211110183934767](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110183934767.png)

![image-20211110184743030](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211110184743030.png)

![image-20211112093621157](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112093621157.png)

![image-20211112093851128](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112093851128.png)

![image-20211112094304963](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112094304963.png)

![image-20211112094846570](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112094846570.png)

![image-20211112094953548](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112094953548.png)

![image-20211112100918999](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112100918999.png)

## 6.2 特征点提取、匹配和光流

![image-20211112102619095](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112102619095.png)

在光流中,我们通常选择角点来追踪。为什么需要角点?

1.角点的作用：方便匹配。梯度在两个方向都有分布。

![image-20211112103849940](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112103849940.png)

![image-20211112104347126](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112104347126.png)

![image-20211112105217633](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112105217633.png)

![image-20211112105237194](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112105237194.png)

![image-20211112105354468](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112105354468.png)

![image-20211112105440844](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112105440844.png)

## 6.3 关键帧与三角化

大部分后端没有那么好的实时性，100-200ms，前端要合理地往后端丢keyframe，

![image-20211112153234284](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112153234284.png)

![image-20211112153919162](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112153919162.png)

![image-20211112154607968](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112154607968.png)

![image-20211112154639490](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112154639490.png)

也可以在任意时刻都计算三角化，不止在插入关键帧时才计算。

![image-20211112155404831](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112155404831.png)

![image-20211112155623920](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112155623920.png)

![image-20211112160357305](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112160357305.png)

![image-20211112162904509](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112162904509.png)

![image-20211112162914721](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112162914721.png)

# 7.VINS系统初始化与VIO系统

## 7.1 VIO相关知识回顾

IMU预积分技术：IMU200Hz，数据会非常多，通常会对IMU数据进行预积分，比如$q_{b_1b_2}$就是$b_1b_2$之间的旋转角速度，$\alpha_{b_1b_2}$表示$b_1b_2$之间的位移增量，$\beta_{b_1b_2}$表示$b_1b_2$之间的速度预积分量。

![image-20211112171835029](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112171835029.png)

**光流：可以预测下一时刻特征点的位置。匹配：通过特征描述子来找到不同图像中的特征点。**

![image-20211112173307167](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112173307167.png)

![image-20211112190923998](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112190923998.png)

## 7.2 VINS鲁棒初始化



![image-20211112191027308](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211112191027308.png)

### 7.2.1 估计外参数旋转$q_{bc}$



### 7.2.2 估计陀螺仪bias



### 7.2.3 估计重力向量，速度和尺度



### 7.2.4 优化重力向量$g^{c_0}$



### 7.2.5 对齐导航世界坐标系$w$



## 7.3 VINS系统

### 7.3.1 VINS系统流程



### 7.3.2 VINS滑动窗口优化