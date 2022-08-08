# 1.向量究竟是什么？

**线性代数中的任何运动都离不开加法与数乘。**

把向量看成是空间中的一种运动。

向量是空间中的箭头

向量是有序的数字列表

# 2.线性组合、张成的空间与基

i与j是xy坐标系的“基向量”

![image-20210908154838056](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908154838056.png)

将单个向量看作箭头

当考虑多个向量时，就把它们都看作点。

![image-20210908155154163](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908155154163.png)

是三维空间中某个过原点的平面

![image-20210908161628304](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908161628304.png)

三个三维向量（第三个向量不在前两个向量的平面上），张成三维空间。

![image-20210908161807809](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908161807809.png)

![image-20210908161940607](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908161940607.png)![image-20210908162040917](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908162040917.png)



# 3.矩阵与线性变换

![image-20210908162526056](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908162526056.png)

它接收输入内容并输出结果。

![image-20210908162645683](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908162645683.png)

==**线性变换的2个特征：**==![image-20210908162832914](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908162832914.png)

![image-20210908162928286](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908162928286.png)

![image-20210908165902320](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908165902320.png)

==**线性变换变的是基。**==

![image-20210908170323773](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908170323773.png)

![image-20210908170708700](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908170708700.png)

![](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908171147911.png)

可以将线性变换看作是对空间的挤压伸展。关键的一点在于，线性变换由它对空间的基向量的作用完全决定。

其他任意向量都能表示为基向量的线性组合。

当你把矩阵看作空间的变换之后，此后几乎所有主题都会有更加直观的理解。

![image-20210908171232872](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908171232872.png)

# 4.矩阵乘法与线性变换复合



两个向量的外积

外积实际上是两个向量围成的平行四边形的有向面积（角度逆时针为正），这个面积实际上是另一个三维向量的长度。

![image-20210908145005522](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908145005522.png)