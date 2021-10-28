# 1.初识SLAM

​	![image-20210909160514115](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909160514115.png)

![image-20211025172325654](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211025172325654.png)

我们把整个视觉 SLAM 流程分为以下几步： 

1. **传感器信息读取**。在视觉 SLAM 中主要为相机图像信息的读取和预处理。如果在机器人中，还可能有码盘、惯性传感器等信息的读取和同步。 
2.  **视觉里程计 (Visual Odometry, VO)**。视觉里程计任务是估算相邻图像间相机的运动， 以及局部地图的样子。VO 又称为前端（Front End）。 
3.  **后端优化（Optimization）**。后端接受不同时刻视觉里程计测量的相机位姿，以及回环检测的信息，对它们进行优化，得到全局一致的轨迹和地图。由于接在 VO 之后， 又称为后端（Back End）。 
4.  **回环检测（Loop Closing）**。回环检测判断机器人是否曾经到达过先前的位置。如果检测到回环，它会把信息提供给后端进行处理。 
5.  **建图（Mapping）**。它根据估计的轨迹，建立与任务要求对应的地图。



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

==**四元数：$q = q_0 + q_1i + q_2j + q_3k$**==

其中i,j,k为四元数的三个虚部，$q_0$为实部

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

==**用李代数表达相机姿态**==

![image-20211026162756456](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026162756456.png)

![image-20211026162931777](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026162931777.png)

![image-20210922201540521](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922201540521.png)

![image-20211026163048646](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026163048646.png)

![image-20211026163137545](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026163137545.png)

# 4.相机与图像

![image-20210909184359208](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210909184359208.png)

相机将三维世界中的坐标点（单位为米）映射到二维图像平面（单位为像素）的过程能够用一个几何模型进行描述。这个模型有很多种，其中最简单的称为针孔模型。针孔模型是很常用，而且有效的模型，它描述了一束光线通过针孔之后，在针孔背面投影成像的关系。在本书中我们用一个简单的针孔相机模型来对这种映射关系进行建模。同时，由于相机镜头上的透镜的存在，会使得光线投影到成像平面的过程中会产生畸变。**==因此，我们使用针孔和畸变两个模型来描述整个投影过程。==**在本节我们先给出相机的针孔模型，再对透镜的畸变模型进行讲解。**这两个模型能够把外部的三维点投影到相机内部成像平面，构成了相机的内参数。**

![image-20211026152939688](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026152939688.png)

![image-20211026152952935](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026152952935.png)

​	读者可能要问,为什么我们可以看似随意地把成像平面挪到前方呢?这只是我们处理真实世界与相机投影的数学手段,并且,大多数相机输出的图像并不是倒像——相机自身的软件会帮你翻转这张图像,所以你看到的一般是正着的像,也就是对称的成像平面上的像。所以,尽管从物理原理来说,小孔成像应该是倒像,但由于我们对图像作了预处理,所以理解成在对称平面上的像,并不会带来什么坏处。于是,在不引起歧义的情况下,我们也不加限制地称后一种情况为针孔模型。
​	式(5.3)描述了点 P 和它的像之间的空间关系。不过,在相机中,我们最终获得的是一个个的像素,这需要在成像平面上对像进行采样和量化。为了描述传感器将感受到的光线转换成图像像素的过程,我们设在物理成像平面上固定着一个像素平面 o − u − v。我们在像素平面得到了 P′ 的像素坐标:[u, v]T 。

![image-20211026154104936](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026154104936.png)

​	除了内参之外,自然还有相对的外参。考虑到在式(5.6)中,我们使用的是 P 在相机坐标系下的坐标。由于相机在运动,所以 P 的相机坐标应该是它的世界坐标(记为 Pw ),根据相机的当前位姿,变换到相机坐标系下的结果。相机的位姿由它的旋转矩阵 R 和平移向量 t 来描述。那么有:

![image-20211026154240499](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026154240499.png)

**畸变**

径向畸变：由透镜形状引起的畸变称之为径向畸变。

切向畸变：除了透镜的形状会引入径向畸变外，在相机的组装过程中由于不能使得透镜和成像面严格平行也会引入切向畸变。

![image-20210913092154114](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913092154114.png)

![image-20210913091131742](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913091131742.png)

## 4.2 双目相机的成像原理

在左右双目的相机中，我们可以把两个相机都看作针孔相机。它们是水平放置的，意味两个相机的光圈中心都位于 x 轴上。它们的距离称为双目相机的基线（Baseline, 记作 b），是双目的重要参数。

![image-20210913144254931](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913144254931.png)

现在，考虑一个空间点 P，它在左眼和右眼各成一像，记作 PL, PR。由于相机基线的存在，这两个成像位置是不同的。理想情况下，由于左右相机只有在 x 轴上有位移，因此P 的像也只在 x 轴（对应图像的 u 轴）上有差异。我们记它在左侧的坐标为 uL，右侧坐标为 uR。那么，它们的几何关系如图5-6右侧所示。根据三角形 P −PL −PR 和 P −OL −OR的相似关系，有：

![image-20210913144815318](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913144815318.png)

![image-20210913144431466](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913144431466.png)

**这里 d 为左右图的横坐标之差，称为视差（Disparity）**。**根据视差，我们可以估计一个像素离相机的距离。**视差与距离成反比：视差越大，距离越近。同时，由于视差最小为一个像素，于是双目的深度存在一个理论上的最大值，由 fb 确定。我们看到，当基线越长时，双目最大能测到的距离就会变远；反之，小型双目器件则只能测量很近的距离。

==注：ZED2、 Intel Realsense D435系列都是用双目（三角测量）的原理计算深度的。==

## 4.3 RGB-D 相机模型

**相比于双目相机通过视差计算深度的方式,RGB-D 相机的做法更为“主动”一些,它能够主动测量每个像素的深度**。目前的 RGB-D 相机按原理可分为两大类:

1. 通过**红外结构光 (Structured Light)**来测量像素距离的。例子有 Kinect 1 代、 ProjectTango 1 代、Intel RealSense 等;

2.  通过**飞行时间法(Time-of-flight, ToF)**原理测量像素距离的。例子有 Kinect 2 代和一些现有的 ToF 传感器等。

  ![image-20211026191332220](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026191332220.png)

​    **无论是结构光还是 ToF,RGB-D 相机都需要向探测目标发射一束光线(通常是红外光)**。在结构光原理中,相机根据返回的结构光图案,计算物体离自身的距离。而在 ToF中,相机向目标发射脉冲光,然后根据发送到返回之间的光束飞行时间,确定物体离自身的距离。ToF 原理和激光传感器十分相似,不过激光是通过逐点扫描来获取距离,而 ToF相机则可以获得整个图像的像素深度,这也正是 RGB-D 相机的特点。所以,如果你把一个 RGB-D 相机拆开,通常会发现除了普通的摄像头之外,至少会有一个发射器和一个接收器。
​    在测量深度之后,RGB-D 相机通常按照生产时的各个相机摆放位置,自己完成深度与彩色图像素之间的配对,输出一一对应的彩色图和深度图。我们可以在同一个图像位置,读取到色彩信息和距离信息,计算像素的 3D 相机坐标,生成点云(Point Cloud)。

​    RGB-D 相机能够实时地测量每个像素点的距离。但是,由于这种发射-接受的测量方式,使得它使用范围比较受限。用红外进行深度值测量的 RGB-D 相机,容易受到日光或其他传感器发射的红外光干扰,因此不能在室外使用,同时使用多个时也会相互干扰。对于透射材质的物体,因为接受不到反射光,所以无法测量这些点的位置。此外,RGB-D 相机在成本、功耗方面,都有一些劣势。

## 4.4 图像

在数学中，图像可以用一个矩阵来描述；而在计算机中，它们占据一段连续的磁盘或内存空间，可以用二维数组来表示。这样一来，程序就不必区别它们处理的是一个数值矩阵，还是有实际意义的图像了。在图像中，数组的行数对应图像的高度，而列数对应图像的宽度。

![image-20210913150242663](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913150242663.png)

![image-20210913151011772](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913151011772.png)

它对应着灰度值 I(x, y) 的读数。请注意这里的 x 和 y 的顺序。虽然我们有些繁琐地向读者讨论坐标系的问题，但是像这种下标顺序的错误，会是新手在调试过程中经常碰到的，又具有一定隐蔽性的错误之一。如果你在写程序时不慎调换了 x, y 的坐标，编译器无法提供任何信息，而你能看到的只是程序运行中的一个越界错误而已。

最常见的彩色图像有三个通道，每个通道都由 8 位整数表示。在这种规定下，一个像素占据了 24 位空间。通道的数量，顺序都是可以自由定义的。**在 OpenCV 的彩色图像中，通道的默认顺序是 B,G,R。**

# 5.非线性优化

![image-20210913150632502](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913150632502.png)

​	在前面几章，我们介绍了经典 SLAM 模型的运动方程和观测方程。现在我们已经知道，**方程中的位姿可以由变换矩阵来描述，然后用李代数进行优化。观测方程由相机成像模型给出，其中内参是随相机固定的，而外参则是相机的位姿。**于是，我们已经弄清了经典 SLAM 模型在视觉情况下的具体表达。
​	然而，由于噪声的存在，运动方程和观测方程的等式必定不是精确成立的。尽管相机可以非常好地符合针孔模型，但遗憾的是，我们得到的数据通常是受各种未知噪声影响的。即使我们有着高精度的相机，运动方程和观测方程也只能近似的成立。所以，与其假设数据必须符合方程，不如来讨论，如何在有噪声的数据中进行准确的状态估计。
​	大多现代视觉 SLAM 算法都不需要那么高成本的传感器，甚至也不需要那么昂贵的处理器来计算这些数据，这全是算法的功劳。由于在 SLAM 问题中，同一个点往往会被一个相机在不同的时间内多次观测，同一个相机在每个时刻观测到的点也不止一个。这些因素交织在一起，使我们拥有了更多的约束，最终能够较好地从噪声数据中恢复出我们需要的东西。本节就将介绍**如何通过优化处理噪声数据，并且由这些表层逐渐深入到图优化本质，提供图优化的解决算法初步介绍并且提供训练实例。**

![image-20210913163740407](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913163740407.png)

![image-20210913164036004](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913164036004.png)

**在这些噪声的影响下，我们希望通过带噪声的数据z 和 u，推断位姿 x 和地图 y（以及它们的概率分布）**，这构成了一个状态估计问题。由于在 SLAM 过程中，这些数据是随着时间逐渐到来的，所以在历史上很长一段时间内，研究者们使用滤波器，尤其是扩展卡尔曼滤波器（EKF）求解它。==卡尔曼滤波器关心当前时刻的状态估计 xk，而对之前的状态则不多考虑；相对的，近年来普遍使用的非线性优化方法，使用所有时刻采集到的数据进行状态估计，并被认为优于传统的滤波器== ，成为当前视觉 SLAM 的主流方法。

![image-20210923094356917](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210923094356917.png)

**状态变量：所有时刻的位姿x，和所有时刻的路标y。**



![image-20210913170021047](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913170021047.png)

![image-20210923112702826](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210923112702826.png)

**可以把slam问题看成是最大似然估计问题，在怎样的状态下，最容易产生当前的观测。**



## 5.1 非线性最小二乘

![image-20210923112837474](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210923112837474.png)

![image-20210923113056884](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210923113056884.png)

![image-20210923113527758](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210923113527758.png)

### 5.1.1 一阶和二阶梯度法

一阶梯度法：最速下降法

![image-20211026201833970](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026201833970.png)

二阶梯度法：牛顿法

![image-20211026201937603](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026201937603.png)

### 5.1.2 Gauss-Newton

![image-20211026202123217](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026202123217.png)

### 5.1.3 Levenberg-Marquadt

列文伯格-马夸尔特法

![image-20211026202142786](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026202142786.png)

## 5.2 Ceres && g2o

本章的第二个实践部分将介绍另一个(主要在 SLAM 领域)广为使用的优化库:g2o(General Graphic Optimization,G2O) 。它是一个基于图优化的库。**图优化是一种将非线性优化与图论结合起来的理论**,因此在使用它之前,我们花一点篇幅介绍一个图优化理论。

### 5.2.1 图优化理论简介

​	我们已经介绍了非线性最小二乘的求解方式。它们是由很多个误差项之和组成的。然而,仅有一组优化变量和许多个误差项,我们并不清楚它们之间的关联。比方说,某一个优化变量 xj 存在于多少个误差项里呢?我们能保证对它的优化是有意义的吗?进一步,我们希望能够直观地看到该优化问题长什么样。于是,就说到了图优化。图优化,是把优化问题表现成图(Graph)的一种方式。这里的图是图论意义上的图。一个图由若干个顶点(Vertex),以及连接着这些节点的边(Edge)组成。进而,用顶点表示优化变量,用边表示误差项。于是,对任意一个上述形式的非线性最小二乘问题,我们可以构建与之对应的一个图。

![image-20211026184802162](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026184802162.png)	

​	图 6-2 是一个简单的图优化例子。我们用三角形表示相机位姿节点,用圆形表示路标点,它们构成了图优化的顶点;同时,蓝色线表示相机的运动模型,红色虚线表示观测模型,它们构成了图优化的边。此时,虽然整个问题的数学形式仍是式(6.12)那样,但现在我们可以直观地看到问题的结构了。如果我们希望,也可以做去掉孤立顶点或优先优化边数较多(或按图论的术语,度数较大)的顶点这样的改进。**但是最基本的图优化,是用图模型来表达一个非线性最小二乘的优化问题。而我们可以利用图模型的某些性质,做更好的优化。**
![image-20211026185257090](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026185257090.png)

1. 定义顶点和边的类型;
2. 构建图;
3. 选择优化算法;
4. 调用 g2o 进行优化,返回结果。

# 6.视觉里程计1

![image-20210913170357761](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210913170357761.png)

## 6.1 特征点法

回顾第二讲的内容，我们说过视觉 SLAM 主要分为视觉前端和优化后端。前端也称为视觉里程计（VO）。它根据相邻图像的信息，估计出粗略的相机运动，给后端提供较好的初始值。**==VO 的实现方法，按是否需要提取特征，分为特征点法的前端以及不提特征的直接法前端==**。基于特征点法的前端，长久以来（直到现在）被认为是视觉里程计的主流方法。**它运行稳定，对光照、动态物体不敏感，是目前比较成熟的解决方案**。在本讲中，我们将从特征点法入手，学习如何提取、匹配图像特征点，然后估计两帧之间的相机运动和场景结构，从而实现一个基本的两帧间视觉里程计。

VO 的主要问题是如何根据图像来估计相机运动。然而，图像本身是一个由亮度和色彩组成的矩阵，如果直接从矩阵层面考虑运动估计，将会非常困难。所以，我们习惯于采用这样一种做法：**首先，从图像中选取比较有代表性的点。这些点在相机视角发生少量变化后会保持不变，所以我们会在各个图像中找到相同的点。**然后，在这些点的基础上，讨论相机位姿估计问题，以及这些点的定位问题。在经典 SLAM 模型中，把它们称为路标。**而在视觉 SLAM 中，路标则是指图像特征（Features）。**

所以最简单的，单个图像像素也是一种“特征”。但是，**在视觉里程计中，我们希望特征点在相机运动之后保持稳定，**而灰度值受光照、形变、物体材质的影响严重，在不同图像之间变化非常大，不够稳定。理想的情况是，当场景和相机视角发生少量改变时，我还能从图像中判断哪些地方是同一个点，因此仅凭灰度值是不够的，我们需要对图像提取特征点。

特征点是图像里一些特别的地方。以图 7-1 为例。我们可以把图像中的角点、边缘和区块都当成图像中有代表性的地方。不过，我们更容易精确地指出，某两幅图像当中出现了同一个角点；同一个边缘则稍微困难一些，因为沿着该边缘前进，图像局部是相似的；同一个区块则是最困难的。我们发现，图像中的角点、边缘相比于像素区块而言更加“特别”，它们不同图像之间的辨识度更强。所以，一种直观的提取特征的方式就是在不同图像间辨认角点，确定它们的对应关系。在这种做法中，角点就是所谓的特征。

![image-20210915151846366](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210915151846366.png)

然而，在大多数应用中，单纯的角点依然不能满足很多我们的需求。例如，从远处看上去是角点的地方，当相机走近之后，可能就不显示为角点了。或者，当我旋转相机时，角点的外观会发生变化，我们也就不容易辨认出那是同一个角点。为此，计算机视觉领域的研究者们在长年的研究中，设计了许多更加稳定的局部图像特征，如著名的 **==SIFT, SURF,ORB==**等等。相比于朴素的角点，这些人工设计的特征点能够拥有如下的性质：

![image-20210915151913911](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210915151913911.png)

特征点由**关键点（Key-point）和描述子（Descriptor）**两部分组成。比方说，当我们谈论 SIFT 特征时，是指“提取 SIFT 关键点，并计算 SIFT 描述子”两件事情。**关键点是指该特征点在图像里的位置**，有些特征点还具有朝向、大小等信息。**描述子通常是一个向量，按照某种人为设计的方式，描述了该关键点周围像素的信息。**描述子是按照“外观相似的特征应该有相似的描述子”的原则设计的。因此，只要两个特征点的描述子在向量空间上的距离相近，就可以认为它们是同样的特征点。

而 ORB(Oriented FAST and Rotated BRIEF)特征则是目前看来非常具有代表性的实时图像特征。它改进了 FAST 检测子不具有方向性的问题,并采用速度极快的二进制描述子BRIEF，使整个图像特征提取的环节大大加速。根据作者在论文中的测试,在同一幅图像中同时提取约 1000 个特征点的情况下, ORB 约要花费 15.3ms, SURF 约花费 217.3ms,SIFT 约花费 5228.7ms。由此可以看出 ORB 在保持了特征子具有旋转,尺度不变性的同时,速度方面提升明显,对于实时性要求很高的 SLAM 来说是一个很好的选择。

### 6.1.1 ORB特征

ORB 特征亦由关键点和描述子两部分组成。它的关键点称为“Oriented FAST”，是一种改进的 FAST 角点，什么是 FAST 角点我们将在下文介绍。它的描述子称为 BRIEF。因此，提取 ORB 特征分为两个步骤：

1. FAST 角点提取：找出图像中的” 角点”。相较于原版的 FAST, ORB 中计算了特征点的主方向，为后续的 BRIEF 描述子增加了旋转不变特性。
2. BRIEF 描述子：对前一步提取出特征点的周围图像区域进行描述。

![image-20210915161426331](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210915161426331.png)

**FAST 是一种角点，主要检测局部像素灰度变化明显的地方，以速度快著称。它的思想是：如果一个像素与它邻域的像素差别较大（过亮或过暗）, 那它更可能是角点。**相比于其他角点检测算法，FAST 只需比较像素亮度的大小，十分快捷。它

![image-20210915161526276](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210915161526276.png)

**FAST 特征点的计算仅仅是比较像素间亮度的差异**，速度非常快，但它也有一些问题。首先，FAST 特征点数量很大且不确定，而我们往往希望对图像提取固定数量的特征。因此，在 ORB 中，对原始的 FAST 算法进行了改进。我们可以指定最终要提取的角点数量N，对原始 FAST 角点分别计算 Harris 响应值，然后选取前 N 个具有最大响应值的角点，作为最终的角点集合。其次，FAST角点不具有方向信息。

### 6.1.2 特征匹配

​	特征匹配是视觉 SLAM 中极为关键的一步,宽泛地说,特征匹配解决了 SLAM 中的**数据关联问题(data association),即确定当前看到的路标与之前看到的路标之间的对应关系**。==通过对图像与图像,或者图像与地图之间的描述子进行准确的匹配==,我们可以为后续的姿态估计,优化等操作减轻大量负担。然而,由于图像特征的局部特性,**误匹配的情况广泛存在,而且长期以来一直没有得到有效解决**,目前已经成为视觉 SLAM 中制约性能提升的一大瓶颈。部分原因是因为场景中经常存在大量的重复纹理,使得特征描述非常相似。在这种情况下,仅利用局部特征解决误匹配是非常困难的。

​	不过,让我们先来看正确匹配的情况,等做完实验再回头去讨论误匹配问题。考虑两个时刻的图像。如果在图像 $I_t$ 中提取到特征点$x^m_t$ ,m = 1, 2, ..., M ,在图像$I_{t+1}$中提取到特征点$x^n_{t+1}$ ,n = 1, 2, ..., N ,如何寻找这两个集合元素的对应关系呢?最简单的特征匹配方法就是**暴力匹配(Brute-Force Matcher)**。即对每一个特征点$x^m_t$与所有的$x^n_{t+1}$测量描述子的距离,然后排序,取最近的一个作为匹配点。**描述子距离表示了两个特征之间的相似程度**,不过在实际运用中还可以取不同的距离度量范数。对于浮点类型的描述子,使用欧氏距离进行度量即可。而对于二进制的描述子(比如 BRIEF 这样的) ,我们往往**使用汉明距离(Hamming distance)做为度量——两个二进制串之间的汉明距离,指的是它们不同位数的个数。**

​	然而,当特征点数量很大时,暴力匹配法的运算量将变得很大,特别是当我们想要匹配一个帧和一张地图的时候。这不符合我们在 SLAM 中的实时性需求。此时**快速近似最近邻(FLANN)算法**更加适合于匹配点数量极多的情况。由于这些匹配算法理论已经成熟,而且实现上也已集成到 OpenCV,所以我们这里就不再描述它的技术细节了。

1. 当相机为单目时,我们只知道 2D 的像素坐标,因而问题是根据两组 2D 点估计运动。该问题用对极几何来解决。
2. 当相机为双目、RGB-D 时,或者我们通过某种方法得到了距离信息,那问题就是根据两组 3D 点估计运动。该问题通常用 ICP 来解决。
3. 如果我们有 3D 点和它们在相机的投影位置,也能估计相机的运动。该问题通过 PnP求解。
因此,下面几节的内容,我们就来介绍这三种情形下的相机运动估计。我们将从最基本的 2D-2D 情形出发,看看它如何求解,求解过程又具有哪些麻烦的问题。

## 6.2 2D-2D:对极几何

### 6.2.1 对极约束

![image-20210922193125748](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922193125748.png)

以图 7-7 为例,我们希望求取两帧图像 I1 , I2 之间的运动,设第一帧到第二帧的运动为R, t。两个相机中心分别为 O1 , O2 。现在,考虑 I1 中有一个特征点 p1 ,它在 I2 中对应着特征点 p2 。我们晓得这俩是通过特征匹配得到的。如果匹配正确,说明它们确实是同一个空间点在两个成像平面上的投影。这里我们需要一些术语来描述它们之间的几何关系。首先，连线$ \overrightarrow{O_1P_1} $和连线$ \overrightarrow{O_2P_2} $在三维空间中会相交于点 P 。这时候点 O1 , O2, P 三个点可以确定一个平面,称为==极平面(Epipolar plane)==。O1 O2 连线与像平面 I1 , I2 的交点分别为 e1 , e2。==e1 , e2,称为极点(Epipoles)==,O1 O2 被称为基线(Baseline)。称极平面与两个像平面 I1 , I 2 之间的相交线 l1 , l2 为**极线(Epipolar line)**。

![image-20210922195226618](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922195226618.png)

![image-20210922195815570](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922195815570.png)

这里 **K 为相机内参矩阵,R, t 为两个坐标系的相机运动(**如果我们愿意,也可以写成李代数形式)

**对极约束简洁地给出了两个匹配点的空间位置关系**。于是，相机位姿估计问题变为以下两步：

**1.根据配对点的像素位置，求出E或者F；**

**2.根据E或者F，求出R,t。**

由于 E 和 F 只相差了相机内参,而内参在 SLAM 中通常是已知的 ,所以实践当中往往使用形式更简单的 E。我们以 E 为例,介绍上面两个问题如何求解。

![image-20211026091417170](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026091417170.png)

![image-20211026091453406](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026091453406.png)

![image-20211026092604967](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026092604967.png)

![image-20211026092755899](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026092755899.png)

## 6.3 三角测量

​	之前两节,我们使用对极几何约束估计了相机运动,也讨论这种方法的局限性。在得到运动之后,下一步我们需要用相机的运动估计特征点的空间位置。在单目 SLAM 中,仅通过单张图像无法获得像素的深度信息,我们需要通过**三角测量(Triangulation) (或三角化)的方法来估计地图点的深度。**

![image-20210922202158742](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922202158742.png)

![image-20210922203139873](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922203139873.png)

**通过两幅图像的特征点（要进行特征匹配），估计出相机的运动（R,t），然后根据R,t计算出图像中的点在世界坐标系下的深度。**

![image-20210922203631553](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922203631553.png)

![image-20210922203606283](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922203606283.png)

![image-20210922203948945](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922203948945.png)

如图 7-10 所示。当平移很小时,像素上的不确定性将导致较大的深度不确定性。也就是说,如果特征点运动一个像素 δx,使得视线角变化了一个角度 δθ,那么测量到深度值将有 δd 的变化。从几何关系可以看到,当 t 较大时,δd 将明显变小,这说明平移较大时,在同样的相机分辨率下,三角化测量将更精确。对该过程的定量分析可以使用正弦定理得到,但我们这里先考虑定性分析。
**因此,要增加三角化的精度,其一是提高特征点的提取精度,也就是提高图像分辨率——但这会导致图像变大,提高计算成本。另一方式是使平移量增大。**但是,平移量增大,会导致图像的外观发生明显的变化,比如箱子原先被挡住的侧面显示出来了,比如反射光发生变化了,等等。外观变化会使得特征提取与匹配变得困难。总而言之,**在增大平移,会导致匹配失效;而平移太小,则三角化精度不够——这就是三角化的矛盾。**
虽然本节只介绍了三角化的深度估计,但只要我们愿意,也能够定量地计算每个特征点的位置及不确定性。所以,如果假设特征点服从高斯分布,并且对它不断地进行观测,在信息正确的情况下,我们就能够期望它的方差会不断减小乃至收敛。这就得到了一个滤波器,称为深度滤波器(Depth Filter)。

## 6.4 3D-2D:PnP

​	**PnP(Perspective-n-Point)**是求解 3D 到 2D 点对运动的方法。它描述了当我们知道**n个3D 空间点以及它们的投影位置**时,如何估计相机所在的位姿。前面已经说了, 2D-2D的对极几何方法需要八个或八个以上的点对(以八点法为例),且存在着初始化、纯旋转和尺度的问题。==然而,如果两张图像中,其中一张特征点的 3D 位置已知==,那么最少只需三个点对(需要至少一个额外点验证结果)就可以估计相机运动。**特征点的 3D 位置可以由三角化,或者由 RGB-D 相机的深度图确定**。因此,**在双目或 RGB-D 的视觉里程计中,我们可以直接使用 PnP 估计相机运动**。而在单目视觉里程计中,必须先进行初始化,然后才能使用 PnP。3D-2D 方法不需要使用对极约束,又可以在很少的匹配点中获得较好的运动估计,是最重要的一种姿态估计方法。

![image-20211026142819069](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026142819069.png)

### 6.4.1 直接线性变换DLT

通过某特征点已知的像素坐标和3D空间坐标，求解出此时相机的位姿$R,t$。

![image-20211026145555611](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026145555611.png)

### 6.4.2 P3P

P3P 是另一种解 PnP 的方法。它仅使用三对匹配点,对数据要求较少,因此这里也简单介绍一下。

![image-20211026150012518](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026150012518.png)

![image-20211026151230561](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026151230561.png)

![image-20211026155235976](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026155235976.png)

### 6.4.3 Bundle Adjustment光束法平差

BA简述：https://blog.csdn.net/OptSolution/article/details/64442962#t6

**BA的本质是一个优化模型，其目的是最小化重投影误差**

bundle,来源于bundle of light,其本意就是指光束，这些光束指的是三维空间的点投影到像平面上的光束，而重投影误差正是利用这些光束构建的，因此称为光束法强调光束也正是描述其优化模型是如何建立的。剩下的就是平差，那什么是平差呢？借用一下百度词条 **测量平差** 中的解释吧。

![image-20211026155312576](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026155312576.png)

![image-20211026204454369](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026204454369.png)

![image-20211026204559173](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026204559173.png)

![image-20211026204936855](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211026204936855.png)

## 6.5 3D-3D:ICP迭代最近点

![image-20211027093300077](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027093300077.png)

![image-20211027100207910](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027100207910.png)

![image-20211027100606586](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027100606586.png)

非线性优化：以迭代的方式寻找最优值。

![image-20211027100654396](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027100654396.png)

## 6.6 实践：求解ICP

![image-20211027103054228](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027103054228.png)

## 6.7 小结

![image-20210922202038220](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210922202038220.png)

# 7.视觉里程计2

![image-20211027103126873](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027103126873.png)

## 7.1 直接法的引出

直接法不再需要特征点匹配。

**1.用光流法来跟踪特征点的运动；**

**2.用直接法来计算关键点在下一时刻图像的位置；**

**3.根据像素灰度的差异，直接计算相机运动。**

![image-20211027105208192](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027105208192.png)

​	直接法是本讲介绍的重点。它是为了克服特征点法的上述缺点而存在的。**直接法根据像素的亮度信息,估计相机的运动,可以完全不用计算关键点和描述子**,于是,既避免了特征的计算时间,也避免了特征缺失的情况。**只要场景中存在明暗变化(可以是渐变,不形成局部的图像梯度) ,直接法就能工作**。**根据使用像素的数量,直接法分为稀疏、稠密和半稠密三种。相比于特征点法只能重构稀疏特征点(稀疏地图) ,直接法还具有恢复稠密或半稠密结构的能力。**

## 7.2 光流(Optical Flow)

![image-20211027111314503](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027111314503.png)

![image-20211027111632704](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027111632704.png)

​	灰度不变假设是一个很强的假设,实际当中很可能不成立。事实上,由于物体的材质不同,像素会出现高光和阴影部分;有时,相机会自动调整曝光参数,使得图像整体变亮或变暗。这些时候灰度不变假设都是不成立的,因此光流的结果也不一定可靠。然而,从另一方面来说,所有算法都是在一定假设下工作的。如果我们什么假设都不做,就没法设计实用的算法。所以,暂且让我们认为该假设成立,看看如何计算像素的运动。

![image-20211027112730115](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027112730115.png)

## 7.3 实践：LK光流

使用 LK 的目的是跟踪特征点。我们对第一张图像提取 FAST 角点,然后用 LK 光流跟踪它们,并画在图中。

![image-20211027144114772](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027144114772.png)

​	最后,我们可以通过光流跟踪的特征点,用 PnP、ICP 或对极几何来估计相机运动,这些方法在上一章中都讲过,我们不再讨论。**总而言之,光流法可以加速基于特征点的视觉里程计算法,避免计算和匹配描述子的过程,但要求相机运动较慢(或采集频率较高)。**

## 7.4 直接法

### 7.4.1 直接法的推导

![image-20211027150541390](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027150541390.png)

​	如图8-3所示,考虑某个空间点 P 和两个时刻的相机。P 的世界坐标为 [X, Y, Z],它在两个相机上成像,记非齐次像素坐标为 p1 , p2 。我们的目标是求第一个相机到第二个相机的相对位姿变换。我们以第一个相机为参照系,设第二个相机旋转和平移为 R, t(对应李代数为 ξ) 。同时,两相机的内参相同,记为 K。为清楚起见,我们列写完整的投影方程:

![image-20211027150626885](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027150626885.png)

### 7.4.2 直接法的讨论

![image-20211027154223180](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027154223180.png)

**相比于特征点法,直接法完全依靠优化来求解相机位姿。**从式(8.16)中可以看到,**==像素梯度引导着优化的方向。如果我们想要得到正确的优化结果,就必须保证大部分像素梯度能够把优化引导到正确的方向。==**
这是什么意思呢?我们不妨设身处地地扮演一下优化算法。假设对于参考图像,我们测量到一个灰度值为 229 的像素。并且,由于我们知道它的深度,可以推断出空间点 P 的位置(图 8-6 中在 I1 中测量到的灰度) 。

![image-20211027172313929](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027172313929.png)

此时我们又得到了一张新的图像,需要估计它的相机位姿。这个位姿是由一个初值不断地优化迭代得到的。假设我们的初值比较差,在这个初值下,空间点 P 投影后的像素灰度值是 126。于是,**这个像素的误差为 229 − 126 = 103**。为了减小这个误差,我们希望**==微调相机的位姿,使像素更亮一些。==**

![image-20211027173052159](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027173052159.png)

![image-20211027173108250](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027173108250.png)

## 7.5 实践：RGB-D的直接法

![image-20211027161338838](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027161338838.png)

# 8.实践：设计前端

![image-20211027161404479](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027161404479.png)

## 8.1 确定基本的数据结构

![image-20211027191818328](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027191818328.png)

1.**配置文件**:在写程序中你会经常遇到各种各样的参数,比如相机的内参、特征点的数量、匹配时选择的比例等等。你可以把这些数写在程序中,但那不是一个好习惯。你会经常修改这些参数,但每次修改后都要重新编译一遍程序。当它们数量越来越多时,修改就变得越来越困难。所以,**更好的方式是在外部定义一个配置文件**,程序运行时读取该配置文件中的参数值。这样,**每次只要修改配置文件内容就行**了,不必对程序本身做任何修改。
2.**坐标变换**:你会经常需要在坐标系间进行坐标变换。例如世界坐标到相机坐标、相机坐标到归一化相机坐标、归一化相机坐标到像素坐标等等。**定义一个类把这些操作都放在一起**将更方便些。

所以下面我们就来定义帧、路标这几个概念,在 C++ 中都以类来表示。**我们尽量保证一个类有单独的头文件和源文件,避免把许多个类放在同一个文件中**。然后,**把函数声明放在头文件,实现放在源文件里(除非函数很短,也可以写在头文件中)** 。我们参照 Google的命名规范,同时考虑尽量以初学者也能看懂的方式来写程序。由于我们的程序是偏向算法而非软件工程的,所以不讨论复杂的类继承关系、接口、模板等等,而更**应该关注算法的正确实现,以及是否便于扩展**。我们会把数据成员设置为公有,尽管这在 C++ 软件设计中是应该避免的,如果读者愿意,也可以把它们改成 private 或 protected 接口,并添加设置和获取接口。在过程较为复杂的算法中,我们会把它分解成若干步骤,例如特征提取和匹配应该分别在不同的函数中实现,这样,当我们想修改算法流程时,就不需要修改整个运行流程,只需调整局部的处理方式即可。

![image-20211027195949485](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211027195949485.png)

![image-20211028095818912](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211028095818912.png)

![image-20211028100022180](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211028100022180.png)

![image-20211028100043462](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211028100043462.png)

![image-20211028105226291](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211028105226291.png)

![image-20211028110033394](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20211028110033394.png)

# 9.后端1

# 10.后端2

# 11.回环检测

# 12.建图