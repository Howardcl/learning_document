# 1.初识SLAM

​	![image-20210909160514115](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909160514115.png)

![image-20210908093455509](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908093455509.png)

我们把整个视觉 SLAM 流程分为以下几步： 

1. 传感器信息读取。在视觉 SLAM 中主要为相机图像信息的读取和预处理。如果在机器人中，还可能有码盘、惯性传感器等信息的读取和同步。 
2.  视觉里程计 (Visual Odometry, VO)。视觉里程计任务是估算相邻图像间相机的运动， 以及局部地图的样子。VO 又称为前端（Front End）。 
3.  后端优化（Optimization）。后端接受不同时刻视觉里程计测量的相机位姿，以及回 环检测的信息，对它们进行优化，得到全局一致的轨迹和地图。由于接在 VO 之后， 又称为后端（Back End）。 
4.  回环检测（Loop Closing）。回环检测判断机器人是否曾经到达过先前的位置。如果检测到回环，它会把信息提供给后端进行处理。 
5.  建图（Mapping）。它根据估计的轨迹，建立与任务要求对应的地图。



常见的编译 cmake 工程的做法是这样

![image-20210908101051660](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908101051660.png)

  在Linux中，库文件分成静态库和动态库两种。静态库以.a作为后缀名，共享库以.so结尾。所有库都是一些函数打包后的集合，差别在于静态库每次被调用都会生成一个副本，而共享库则只有一个副本，更省空间。

​	库文件是一个压缩包，里面有编译好的二进制函数。不过，如果仅有.a或.so库文件，那么我们并不知道里面的函数到底是什么，调用的形式又是什么样。为了让别人（或者自己）使用这个库，我们需要提供一个头文件，说明这些库里都有些什么。因此，对于库的使用者，**只要拿到了头文件和库文件，就可以调用这个库了**。

cmake过程处理了工程文件之间的关系，而make实际调用了g++来编译程序。

``` c++
# 将库文件链接到可执行程序上
target_link_libraries( useHello hello_shared )
```

# 2.三维空间刚体运动

**==三维空间的刚体运动描述方式：旋转矩阵、变换矩阵、四元数和欧拉角。==**

线性代数库Eigen：它提供了c++中的矩阵运算，并且它的Geometry模块还提供了四元数等刚体运动的描述。

相比于其他库，Eigen的特殊之处在于，它是一个纯用头文件搭建起来的库。

因为Eigen库只有头文件，所以不需要再用target_link_libraries语句将程序链接到库上。

==**Eigen代数模块**==

``` c++
    // Eigen 中所有向量和矩阵都是Eigen::Matrix，它是一个模板类。它的前三个参数为：数据类型，行，列
    // 声明一个2*3的float矩阵
    Eigen::Matrix<float, 2, 3> matrix_23;

    // 同时，Eigen 通过 typedef 提供了许多内置类型，不过底层仍是Eigen::Matrix
    // 例如 Vector3d 实质上是 Eigen::Matrix<double, 3, 1>，即三维向量
    Eigen::Vector3d v_3d;
	// 这是一样的
    Eigen::Matrix<float,3,1> vd_3d;

    // Matrix3d 实质上是 Eigen::Matrix<double, 3, 3>
    Eigen::Matrix3d matrix_33 = Eigen::Matrix3d::Zero(); //初始化为零
    // 如果不确定矩阵大小，可以使用动态大小的矩阵
    Eigen::Matrix< double, Eigen::Dynamic, Eigen::Dynamic > matrix_dynamic;
    // 更简单的
    Eigen::MatrixXd matrix_x;
```

Eigen矩阵不支持自动类型提升，这和c++的內建数据类型有较大差异。在C++程序中，我们可以把一个float类型和double类型相加、相乘，**编译器会自动把数据类型转换成最合适的那种。而在Eigen中，出于性能的考虑，必须显示地对矩阵类型进行转换。**

旋转矩阵有一些特别的性质。事实上，它是一个行列式为 1 的正交矩阵。反之，行列式为 1 的正交矩阵也是一个旋转矩阵。所以，我们可以把旋转矩阵的集合定义如下：

![image-20210908192545322](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908192545322.png)

**变换矩阵与齐次坐标**

![image-20210908193345281](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908193345281.png)

![image-20210908193533152](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908193533152.png)

==**旋转向量与欧拉角**==

我们希望有一种方式能够紧凑地描述旋转和平移。例如，用一个三维向量表达旋转，用六维向量表达变换，可行吗？事实上，这件事我们在前面介绍外积的那部分，提到过这件事如何做。我们介绍了如何用外积表达两个向量的旋转关系。对于坐标系的旋转，我们知道，任意旋转都可以用一个旋转轴和一个旋转角来刻画。于是，==**我们可以使用一个向量，其方向与旋转轴一致，而长度等于旋转角。这种向量，称为旋转向量**（或轴角，Axis-Angle）==。这种表示法只需一个三维向量即可描述旋转。同样，对于变换矩阵，我们使用**一个旋转向量和一个平移向量即可表达一次变换**。这时的维数正好是六维。
事实上，旋转向量就是我们下章准备介绍的李代数。

剩下的问题是，旋转向量和旋转矩阵之间是如何转换的呢？假设有一个旋转轴为 n，角度为 θ 的旋转，显然，它对应的旋转向量为 θn。由旋转向量到旋转矩阵的过程由罗德里格斯公式（Rodrigues’s Formula ）表明，由于推导过程比较复杂，我们不作描述，只给出转换的结果①：

![image-20210908202243859](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908202243859.png)

![image-20210909103750521](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909103750521.png)

![image-20210909103806150](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909103806150.png)

欧拉角的一个重大缺点是会碰到著名的==万向锁问题（Gimbal Lock）==：==在俯仰角为±90◦ 时，第一次旋转与第三次旋转将使用同一个轴==，使得系统丢失了一个自由度（由三次旋转变成了两次旋转）。这被称为奇异性问题，在其他形式的欧拉角中也同样存在。

![image-20210909111415504](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909111415504.png)

理论上可以证明，只要我们想用三个实数来表达三维旋转时，都会不可避免地碰到奇异性问题。由于这种原理，欧拉角不适于插值和迭代，往往只用于人机交互中。我们也很少在 SLAM程序中直接使用欧拉角表达姿态，同样不会在滤波或优化中使用欧拉角表达旋转（因为它具有奇异性）。不过，若你想验证自己算法是否有错时，转换成欧拉角能够快速辨认结果的正确与否。

![image-20210909105128799](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909105128799.png)

四元数表达的好处是可以避免描述旋转顺序的问题，也可以避免出现万向锁的问题。在设计控制器的时候跟轴角转换时也很方便。

==**四元数：**==


$$
q = q_0 + q_1i + q_2j + q_3k
$$
其中i,j,k为四元数的三个虚部，q0为实部

![image-20210909112207952](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909112207952.png)

有时人们也用一个标量和一个向量来表达四元数：
$$
q=[s,v], s = q_0\in R,	v = [q_1,q_2,q_3]^T \in R^3
$$
这里，s称为四元数的实部，而v称为它的虚部。如果一个四元数的虚部为0，称之为实四元数。反之，若它的实部为0，则称之为虚四元数。

这和复数非常相似。考虑到三维空间需要3个轴，四元数也有3个虚部，那么，一个虚四元数能不能对应到一个空间点呢？

==我们能用**单位四元数**表示三维空间中任意一个旋转。==

假设某个旋转是绕单位向量
$$
n = [n_x,n_y,n_z]^T
$$
进行了角度为 θ的旋转，那么这个旋转的四元数表示为
$$
q = [cos \frac {\theta}{2},n_xsin \frac{\theta}{2},n_ysin \frac{\theta}{2},n_zsin \frac{\theta}{2}]^T
$$
![image-20210909144030880](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909144030880.png)

任意的旋转都可以用两个互为相反数的四元数表示。

![image-20210909145845983](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909145845983.png)

![image-20210909150055818](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909150055818.png)

==**Eigen几何模块**==

``` c++
    // Eigen/Geometry 模块提供了各种旋转和平移的表示
    // 3D 旋转矩阵直接使用 Matrix3d 或 Matrix3f
    Eigen::Matrix3d rotation_matrix = Eigen::Matrix3d::Identity();
    // 旋转向量使用 AngleAxis, 它底层不直接是Matrix，但运算可以当作矩阵（因为重载了运算符）
    Eigen::AngleAxisd rotation_vector ( M_PI/4, Eigen::Vector3d ( 0,0,1 ) );     //沿 Z 轴旋转 45 度
    cout .precision(3);
    cout<<"rotation matrix =\n"<<rotation_vector.matrix() <<endl;                //用matrix()转换成矩阵
    // 也可以直接赋值
    rotation_matrix = rotation_vector.toRotationMatrix();
    // 用 AngleAxis 可以进行坐标变换
    Eigen::Vector3d v ( 1,0,0 );
    Eigen::Vector3d v_rotated = rotation_vector * v;
    cout<<"(1,0,0) after rotation = "<<v_rotated.transpose()<<endl;
    // 或者用旋转矩阵
    v_rotated = rotation_matrix * v;
    cout<<"(1,0,0) after rotation = "<<v_rotated.transpose()<<endl;

    // 欧拉角: 可以将旋转矩阵直接转换成欧拉角
    Eigen::Vector3d euler_angles = rotation_matrix.eulerAngles ( 2,1,0 ); // ZYX顺序，即yaw pitch roll顺序
    cout<<"yaw pitch roll = "<<euler_angles.transpose()<<endl;

    // 欧氏变换矩阵使用 Eigen::Isometry
    Eigen::Isometry3d T=Eigen::Isometry3d::Identity();                // 虽然称为3d，实质上是4＊4的矩阵
    T.rotate ( rotation_vector );                                     // 按照rotation_vector进行旋转
    T.pretranslate ( Eigen::Vector3d ( 1,3,4 ) );                     // 把平移向量设成(1,3,4)
    cout << "Transform matrix = \n" << T.matrix() <<endl;

    // 用变换矩阵进行坐标变换
    Eigen::Vector3d v_transformed = T*v;                              // 相当于R*v+t
    cout<<"v tranformed = "<<v_transformed.transpose()<<endl;

    // 对于仿射和射影变换，使用 Eigen::Affine3d 和 Eigen::Projective3d 即可，略

    // 四元数
    // 可以直接把AngleAxis赋值给四元数，反之亦然
    Eigen::Quaterniond q = Eigen::Quaterniond ( rotation_vector );
    cout<<"quaternion = \n"<<q.coeffs() <<endl;   // 请注意coeffs的顺序是(x,y,z,w),w为实部，前三者为虚部
    // 也可以把旋转矩阵赋给它
    q = Eigen::Quaterniond ( rotation_matrix );
    cout<<"quaternion = \n"<<q.coeffs() <<endl;
    // 使用四元数旋转一个向量，使用重载的乘法即可
    v_rotated = q*v; // 注意数学上是qvq^{-1}
    cout<<"(1,0,0) after rotation = "<<v_rotated.transpose()<<endl;
```

以双精度为例，各种形式的数据类型总结如下：

```c++
旋转矩阵(3*3)	Eigen::Matrix3d
旋转向量(3*1)	Eigen::AngleAxisd
欧拉角(3*1)	Eigen::Vector3d
四元数(4*1)	Eigen::Quaterniond
欧氏变换矩阵(4*4)	Eigen::Isometry3d
仿射变换(4*4)	Eigen::Afine3d
射影变换(4*4)	Eigen::Projective3d	
```



# 3.李群与李代数

![image-20210909160636185](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909160636185.png)

**==三维旋转矩阵构成了特殊正交群SO(3)，而变换矩阵构成了特殊欧氏群SE(3):==**

群对于加法是不封闭的。

SO(3)和SE(3)对于乘法是封闭的：

![image-20210909160730981](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909160730981.png)

**==乘法对应着旋转或变换的复合，两个旋转矩阵相乘表示做了两次旋转。对于这种只有一个运算的集合，我们称之为群。==**

![image-20210909161706587](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909161706587.png)

![image-20210909162624261](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909162624261.png)

![image-20210909173052103](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909173052103.png)

# 4.相机与图像

![image-20210909184359208](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909184359208.png)

相机将三维世界中的坐标点（单位为米）映射到二维图像平面（单位为像素）的过程能够用一个几何模型进行描述。这个模型有很多种，其中最简单的称为针孔模型。针孔模型是很常用，而且有效的模型，它描述了一束光线通过针孔之后，在针孔背面投影成像的关系。在本书中我们用一个简单的针孔相机模型来对这种映射关系进行建模。同时，由于相机镜头上的透镜的存在，会使得光线投影到成像平面的过程中会产生畸变。**==因此，我们使用针孔和畸变两个模型来描述整个投影过程。==**在本节我们先给出相机的针孔模型，再对透镜的畸变模型进行讲解。**这两个模型能够把外部的三维点投影到相机内部成像平面，构成了相机的内参数。**

**畸变**

径向畸变：由透镜形状引起的畸变称之为径向畸变。

切向畸变：除了透镜的形状会引入径向畸变外，在相机的组装过程中由于不能使得透镜和成像面严格平行也会引入切向畸变。

![image-20210913092154114](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913092154114.png)

![image-20210913091131742](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913091131742.png)

==**双目相机的成像原理**==

在左右双目的相机中，我们可以把两个相机都看作针孔相机。它们是水平放置的，意味两个相机的光圈中心都位于 x 轴上。它们的距离称为双目相机的基线（Baseline, 记作 b），是双目的重要参数。

![image-20210913144254931](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913144254931.png)

现在，考虑一个空间点 P，它在左眼和右眼各成一像，记作 PL, PR。由于相机基线的存在，这两个成像位置是不同的。理想情况下，由于左右相机只有在 x 轴上有位移，因此P 的像也只在 x 轴（对应图像的 u 轴）上有差异。我们记它在左侧的坐标为 uL，右侧坐标为 uR。那么，它们的几何关系如图5-6右侧所示。根据三角形 P −PL −PR 和 P −OL −OR的相似关系，有：

![image-20210913144815318](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913144815318.png)

![image-20210913144431466](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913144431466.png)

**这里 d 为左右图的横坐标之差，称为视差（Disparity）**。根据视差，我们可以估计一个像素离相机的距离。视差与距离成反比：视差越大，距离越近。同时，由于视差最小为一个像素，于是双目的深度存在一个理论上的最大值，由 fb 确定。我们看到，当基线越长时，双目最大能测到的距离就会变远；反之，小型双目器件则只能测量很近的距离。

**==图像==**

在数学中，图像可以用一个矩阵来描述；而在计算机中，它们占据一段连续的磁盘或内存空间，可以用二维数组来表示。这样一来，程序就不必区别它们处理的是一个数值矩阵，还是有实际意义的图像了。在图像中，数组的行数对应图像的高度，而列数对应图像的宽度。

![image-20210913150242663](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913150242663.png)

![image-20210913151011772](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913151011772.png)

它对应着灰度值 I(x, y) 的读数。请注意这里的 x 和 y 的顺序。虽然我们有些繁琐地向读者讨论坐标系的问题，但是像这种下标顺序的错误，会是新手在调试过程中经常碰到的，又具有一定隐蔽性的错误之一。如果你在写程序时不慎调换了 x, y 的坐标，编译器无法提供任何信息，而你能看到的只是程序运行中的一个越界错误而已。

最常见的彩色图像有三个通道，每个通道都由 8 位整数表示。在这种规定下，一个像素占据了 24 位空间。通道的数量，顺序都是可以自由定义的。在 OpenCV 的彩色图像中，通道的默认顺序是 B,G,R。

# 5.非线性优化

![image-20210913150632502](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913150632502.png)

​	在前面几章，我们介绍了经典 SLAM 模型的运动方程和观测方程。现在我们已经知道，方程中的位姿可以由变换矩阵来描述，然后用李代数进行优化。观测方程由相机成像模型给出，其中内参是随相机固定的，而外参则是相机的位姿。于是，我们已经弄清了经典 SLAM 模型在视觉情况下的具体表达。
​	然而，由于噪声的存在，运动方程和观测方程的等式必定不是精确成立的。尽管相机可以非常好地符合针孔模型，但遗憾的是，我们得到的数据通常是受各种未知噪声影响的。即使我们有着高精度的相机，运动方程和观测方程也只能近似的成立。所以，与其假设数据必须符合方程，不如来讨论，如何在有噪声的数据中进行准确的状态估计。
​	大多现代视觉 SLAM 算法都不需要那么高成本的传感器，甚至也不需要那么昂贵的处理器来计算这些数据，这全是算法的功劳。由于在 SLAM 问题中，同一个点往往会被一个相机在不同的时间内多次观测，同一个相机在每个时刻观测到的点也不止一个。这些因素交织在一起，使我们拥有了更多的约束，最终能够较好地从噪声数据中恢复出我们需要的东西。本节就将介绍如何通过优化处理噪声数据，并且由这些表层逐渐深入到图优化本质，提供图优化的解决算法初步介绍并且提供训练实例。

![image-20210913163740407](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913163740407.png)

![image-20210913164036004](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913164036004.png)

在这些噪声的影响下，我们希望通过带噪声的数据 z 和 u，推断位姿 x 和地图 y（以及它们的概率分布），这构成了一个状态估计问题。由于在 SLAM 过程中，这些数据是随着时间逐渐到来的，所以在历史上很长一段时间内，研究者们使用滤波器，尤其是扩展卡尔曼滤波器（EKF）求解它。==卡尔曼滤波器关心当前时刻的状态估计 xk，而对之前的状态则不多考虑；相对的，近年来普遍使用的非线性优化方法，使用所有时刻采集到的数据进行状态估计，并被认为优于传统的滤波器== ，成为当前视觉 SLAM 的主流方法。

![image-20210913170021047](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913170021047.png)





# 6.视觉里程计

![image-20210913170357761](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913170357761.png)