# 1.初识SLAM

​	![image-20210908093455509](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210908093455509.png)

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

==**四元数：**==
$$
q = q_0 + q_1i + q_2j + q_3k
$$
其中i,j,k为四元数的三个虚部，q0为实部

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
进行了角度为\theta的旋转，那么这个旋转的四元数表示为
$$
q = [cos \frac {\theta}{2},n_xsin \frac{\theta}{2},n_ysin \frac{\theta}{2},n_zsin \frac{\theta}{2}]^T
$$
任意的旋转都可以用两个互为相反数的四元数表示。



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
    Eigen::Vector3d euler_angles = rotation_matrix.eulerAngles ( 2,1,0 ); // ZYX顺序，即roll pitch yaw顺序
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

三维旋转矩阵构成了特殊正交群SO(3)，而变换矩阵构成了特殊欧氏群SE(3):

群对于加法是不封闭的。

SO(3)和SE(3)对于乘法是封闭的：

乘法对应着旋转或变换的复合，两个旋转矩阵相乘表示做了两次旋转。对于这种只有一个运算的集合，我们称之为群。