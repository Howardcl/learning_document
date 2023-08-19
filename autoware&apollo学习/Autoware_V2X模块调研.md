# 1.Autoware.universe的V2X模块调研

## 1.1 什么是V2X

“V2X”，全称 “Vehicle to Everything”，顾名思义“交通工具与所有事物的联系”。那么究竟是和哪些事物之间发生联系？为什么要发生联系？何时发生什么样的联系呢？

首先，V2X主要包括==V2V 车与车(vehicle)，V2I 车与基础设施(vechile to infrainstructure)，V2P 车与人(vehicle to people)，V2N 车与云(vehicle to network)。==详细而言就是车辆通过传感器，网络通信技术与其它周边车、人、物进行通讯交流，并根据收集的信息进行分析、决策的一项技术。

## 1.2 V2X的作用

那么V2X会给我们的生活带来什么样的变化呢？

首先，对于车联网而言，其第一大类应用，==就是提供车辆上网功能==。这种功能通过车载T-Box实现，目前已经很普及了。什么OTA啊、各种联网车机应用啊皆属此类。

第二大类应用，是==通过车-路-人互联，为汽车提供一个全新的感知维度，或者说提供“上帝视角”，以播报安全预警、提升辅助驾驶的安全性和稳定性、识别[corner case](https://www.zhihu.com/search?q=corner case&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A"466626253"})、助力高级别自动驾驶尽早落地。==

此类应用中目前宣传的比较多、也最容易落地的一个例子是“绿波车速引导”，即通过读取前方红绿灯的剩余时间（需要路口装有路侧通信单元）确定一个能够不停车通过十字路口的车速，提示驾驶员顺畅通过。

那么我们可以设想到，V2X进而可以减少交通事故，降低交通拥堵提高交通效率，减少汽车污染物的排放等等。

第三大类应用，==V2X也是实现自动驾驶的重要手段，能够弥补摄像头、雷达等车载传感器视距不足等缺陷，并且提高车辆在交叉口、恶劣天气环境等特殊条件下的感知能力。==

## 1.3 V2X的技术标准

首先，为统一异构的设备与数据，V2X目前有两种主流的技术标准。

1. DSRC（Dedicated Short Range Communications专用短距离通讯），这个标准是由美国推出的，与wifi类似，在测试中最大传输距离可达300米。
2. LTE-V2X(基于蜂窝移动通信的V2X)，这种技术由中国的大唐与华为主导开发，LTE V2X针对车辆应用定义了两种通信方式：集中式（LTE-V-Cell）和分布式（LTE-V-Direct）。集中式也称为蜂窝式，需要基站作为控制中心，集中式定义车辆与路侧通信单元以及基站设备的通信方式；分布式也称为直通式，无需基站作为支撑，在一些文献中也表示为LTE-Direct（LTE-D）及LTE D2D（Device-to-Device），分布式定义车辆之间的通信方式。



![image-20230814085133988](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308140851161.png)

## 1.4 Autoware V2X模块

### 1.4.1 AutowareV2X设计架构

实现的系统架构如下所示。AutowareV2X基于ETSI C-ITS协议套件[Vanetza](https://github.com/riebl/vanetza)，可以通过以太网接口集成到Autoware中。Autoware 提供的任何信息都可以被提取并打包到以 V2X 消息形式传输的数据包中。由于 Autoware 和 AutowareV2X 都是松散解耦的，因此这两个组件可以放置在单独的硬件上以适应更多用例。

*V2XNode*充当V2X通信堆栈和基于ROS2的Autoware之间的接口，而*V2XApp*则负责V2X通信、跨层网络配置以及CAM和CPM等各种设施的管理所需的常见任务。集体**感知服务（CPS）**也被实现为一个应用程序来演示 AutowareV2X 的用例，并且使得集体感知消息Collective Perception Messages（CPM）的传播和接收成为可能。通过CPM共享的物体信息可以立即输入到Autoware的感知或规划模块中，从而实现CAV的端到端实验和评估。

![image-20230814091841544](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308140918648.png)

RSU:路侧单元

Collective Perception Message (CPM)：集中式感知消息，应该是这几个作者自己定义了这样一种消息格式，用于传输共享目标信息。

![image-20230814141453073](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308141414174.png)

### 1.4.2 双通道冗余感知

autoware v2x包括一种称为“双通道混合交付系统”的双通道集体感知机制，使cpm共享的关键对象信息具有链路冗余。

就是两套系统，一套4G，一套wifi传输。近距离时使用wifi传输信号，远距离时使用4G/LTE传输信号。

当wifi失效时，可以通过4G传输。

![image-20230814151315418](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308141513481.png)

### 1.4.3 通信延迟

使用真实硬件的现场实验表明，Autoware v2x可以在约30 ms的时间内在RSU和CAV之间传递感知信息。AutowareV2X使CAV能够感知物理盲点后面的物体，我们已经通过行人和非联网车辆的场景展示了其应用的有效性。当基于wi - fi的CPM的PDR降低时，双通道CPM的传递也被证明是有效的，使CAV能够根据两个链路收到的CPM信息的新鲜度，从两个链路收到的CPM中动态地选择最佳CPM。

# 2. AutowareV2X模块安装过程

## 2.1 在仿真模拟器中安装 AutowareV2X

在实际现场测试之前，模拟是验证 AutowareV2X 功能的一种简单方法。

[AutowareV2X 可以使用Autoware 的规划模拟器](https://autowarefoundation.github.io/autoware-documentation/main/tutorials/ad-hoc-simulation/planning-simulation/)在模拟环境中运行。ITS-S由作为自动驾驶堆栈的Autoware和作为其V2X通信堆栈的AutowareV2X组成。每个 ITS-S 都在 Docker 容器内执行，ITS-S 之间的无线通信介质采用 Docker 网络进行建模。动态 ITS-S 被定义为 CAV，而静态 ITS-S 被视为 RSU。感知对象作为 CPM 在网络上发送。

为了测试发送方和接收方功能，我们至少需要两个 ITS-S 实例。

### 2.1.1 创建的 Docker 环境

我们将创建如下图所示的 Docker 环境。将有两个 Docker 容器来代表两个 ITS-S，每个容器都包含 Autoware.universe 和 AutowareV2X。它们都将成为 Docker 网络的一部分，称为`v2x_net`“子网” `10.0.0.0/24`。“Autoware Container#1”和“Autoware Container#2”将分别被描述为`autoware_1`和`autoware_2`。

![Docker环境](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308141040870.png)

### 2.1.2 创建用于 V2X 通信的 Docker 网络

```bash
docker network create --driver=bridge --subnet=10.0.0.0/24 v2x_net -o com.docker.network.bridge.name="v2x_net"
```

### 2.1.3 启动两个 ITS-S 容器

[在这里，我们将使用名为off-your-rocker 的](https://github.com/sloretz/off-your-rocker)Rocker 扩展。`off-your-rocker`通过运行以下命令 进行安装：

```bash
python3 -m pip install off-your-rocker
```

在一个终端中，使用rocker启动容器`autoware_1`：(下列命令行均以本人电脑为示例，使用者需将`/home/ubuntu22/autoware_main`路径替换为自己的autoware源码路径，还需将`/home/ubuntu22/autoware_map`路径替换为自己下载的地图路径。)

```bash
rocker --nvidia --x11 --user --privileged --volume /home/ubuntu22/autoware_main --volume /home/ubuntu22/autoware_map --network=v2x_net --name autoware_1 --oyr-run-arg "--ip 10.0.0.2 --hostname autoware_1" -- ghcr.io/autowarefoundation/autoware-universe:latest-cuda
```

在另一个终端中，使用rocker启动容器`autoware_2`：

```bash
rocker --nvidia --x11 --user --privileged --volume /home/ubuntu22/autoware_main --volume /home/ubuntu22/autoware_map --network=v2x_net --name autoware_2 --oyr-run-arg "--ip 10.0.0.3 --hostname autoware_2" -- ghcr.io/autowarefoundation/autoware-universe:latest-cuda
```

成功启动后，您应该看到如下输出(以`autoware_2`容器为例)：

```bash
Extension oyr_cap_add doesn't support default arguments. Please extend it.
Extension oyr_cap_drop doesn't support default arguments. Please extend it.
Extension oyr_colcon doesn't support default arguments. Please extend it.
Extension oyr_mount doesn't support default arguments. Please extend it.
Extension oyr_run_arg doesn't support default arguments. Please extend it.
Extension oyr_spacenav doesn't support default arguments. Please extend it.
Extension volume doesn't support default arguments. Please extend it.
Active extensions ['name', 'network', 'nvidia', 'oyr_run_arg', 'privileged', 'volume', 'x11', 'user']
Step 1/6 : FROM golang:1.19 as detector
 ---> b95d19c099a7
Step 2/6 : RUN git clone -q https://github.com/dekobon/distro-detect.git &&     cd distro-detect &&     git checkout -q 5f5b9c724b9d9a117732d2a4292e6288905734e1 &&     CGO_ENABLED=0 go build .
 ---> Using cache
 ---> 943df15427e4
Step 3/6 : FROM ghcr.io/autowarefoundation/autoware-universe:latest-cuda
 ---> 08edefe59662
Step 4/6 : COPY --from=detector /go/distro-detect/distro-detect /tmp/detect_os
 ---> 28564d633c6f
Step 5/6 : ENTRYPOINT [ "/tmp/detect_os", "-format", "json-one-line" ]
 ---> Running in 8e831eb5cde7
Removing intermediate container 8e831eb5cde7
 ---> 25aa2654b6af
Step 6/6 : CMD [ "" ]
 ---> Running in d9230ca40b68
Removing intermediate container d9230ca40b68
 ---> 533e6a3e2abc
Successfully built 533e6a3e2abc
Successfully tagged rocker:os_detect_ghcr.io_autowarefoundation_autoware-universe_latest-cuda
running,  docker run -it --rm 533e6a3e2abc
output:  {"name":"Ubuntu","id":"ubuntu","version":"22.04","lsb_release":{"DISTRIB_CODENAME":"jammy","DISTRIB_DESCRIPTION":"Ubuntu 22.04.2 LTS","DISTRIB_ID":"Ubuntu","DISTRIB_RELEASE":"22.04"},"os_release":{"BUG_REPORT_URL":"https://bugs.launchpad.net/ubuntu/","HOME_URL":"https://www.ubuntu.com/","ID":"ubuntu","ID_LIKE":"debian","NAME":"Ubuntu","PRETTY_NAME":"Ubuntu 22.04.2 LTS","PRIVACY_POLICY_URL":"https://www.ubuntu.com/legal/terms-and-policies/privacy-policy","SUPPORT_URL":"https://help.ubuntu.com/","UBUNTU_CODENAME":"jammy","VERSION":"22.04.2 LTS (Jammy Jellyfish)","VERSION_CODENAME":"jammy","VERSION_ID":"22.04"}}

Writing dockerfile to /tmp/tmpbu1wzdgi/Dockerfile
vvvvvv
# Preamble from extension [name]

# Preamble from extension [network]

# Preamble from extension [nvidia]
# Ubuntu 16.04 with nvidia-docker2 beta opengl support
FROM nvidia/opengl:1.0-glvnd-devel-ubuntu18.04 as glvnd

# Preamble from extension [oyr_run_arg]
# Preamble from extension [privileged]
# Preamble from extension [volume]
# Preamble from extension [x11]
# Preamble from extension [user]

FROM ghcr.io/autowarefoundation/autoware-universe:latest-cuda
USER root
# Snippet from extension [name]

# Snippet from extension [network]

# Snippet from extension [nvidia]
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libgles2 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=glvnd /usr/share/glvnd/egl_vendor.d/10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json


ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:-all}

# Snippet from extension [oyr_run_arg]

# Snippet from extension [privileged]

# Snippet from extension [volume]

# Snippet from extension [x11]

# Snippet from extension [user]
# make sure sudo is installed to be able to give user sudo access in docker
RUN if ! command -v sudo >/dev/null; then \
      apt-get update \
      && apt-get install -y sudo \
      && apt-get clean; \
    fi

RUN existing_user_by_uid=`getent passwd "1000" | cut -f1 -d: || true` && \
    if [ -n "${existing_user_by_uid}" ]; then userdel -r "${existing_user_by_uid}"; fi && \
    existing_user_by_name=`getent passwd "ubuntu22" | cut -f1 -d: || true` && \
    existing_user_uid=`getent passwd "ubuntu22" | cut -f3 -d: || true` && \
    if [ -n "${existing_user_by_name}" ]; then find / -uid ${existing_user_uid} -exec chown -h 1000 {} + || true ; find / -gid ${existing_user_uid} -exec chgrp -h 1000 {} + || true ; fi && \
    if [ -n "${existing_user_by_name}" ]; then userdel -r "${existing_user_by_name}"; fi && \
    existing_group_by_gid=`getent group "1000" | cut -f1 -d: || true` && \
    if [ -z "${existing_group_by_gid}" ]; then \
      groupadd -g "1000" "ubuntu22"; \
    fi && \
    useradd --no-log-init --no-create-home --uid "1000" -s /bin/bash -c "ubuntu22,,," -g "1000" -d "/home/ubuntu22" "ubuntu22" && \
    echo "ubuntu22 ALL=NOPASSWD: ALL" >> /etc/sudoers.d/rocker

# Making sure a home directory exists if we haven't mounted the user's home directory explicitly
RUN mkdir -p "$(dirname "/home/ubuntu22")" && mkhomedir_helper ubuntu22
# Commands below run as the developer user
USER ubuntu22
WORKDIR /home/ubuntu22


^^^^^^
Building docker file with arguments:  {'path': '/tmp/tmpbu1wzdgi', 'rm': True, 'nocache': False, 'pull': False}
building > Step 1/12 : FROM nvidia/opengl:1.0-glvnd-devel-ubuntu18.04 as glvnd
building >  ---> 9d806b36b807
building > Step 2/12 : FROM ghcr.io/autowarefoundation/autoware-universe:latest-cuda
building >  ---> 08edefe59662
building > Step 3/12 : USER root
building >  ---> Using cache
building >  ---> c3da44850b35
building > Step 4/12 : RUN apt-get update && apt-get install -y --no-install-recommends     libglvnd0     libgl1     libglx0     libegl1     libgles2     && rm -rf /var/lib/apt/lists/*
building >  ---> Using cache
building >  ---> 547bf2d23d93
building > Step 5/12 : COPY --from=glvnd /usr/share/glvnd/egl_vendor.d/10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json
building >  ---> Using cache
building >  ---> cde5b72c6dd7
building > Step 6/12 : ENV NVIDIA_VISIBLE_DEVICES ${NVIDIA_VISIBLE_DEVICES:-all}
building >  ---> Using cache
building >  ---> 1f28be77556a
building > Step 7/12 : ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES:-all}
building >  ---> Using cache
building >  ---> 6a66048f7aa9
building > Step 8/12 : RUN if ! command -v sudo >/dev/null; then       apt-get update       && apt-get install -y sudo       && apt-get clean;     fi
building >  ---> Using cache
building >  ---> 62b30f25ab95
building > Step 9/12 : RUN existing_user_by_uid=`getent passwd "1000" | cut -f1 -d: || true` &&     if [ -n "${existing_user_by_uid}" ]; then userdel -r "${existing_user_by_uid}"; fi &&     existing_user_by_name=`getent passwd "ubuntu22" | cut -f1 -d: || true` &&     existing_user_uid=`getent passwd "ubuntu22" | cut -f3 -d: || true` &&     if [ -n "${existing_user_by_name}" ]; then find / -uid ${existing_user_uid} -exec chown -h 1000 {} + || true ; find / -gid ${existing_user_uid} -exec chgrp -h 1000 {} + || true ; fi &&     if [ -n "${existing_user_by_name}" ]; then userdel -r "${existing_user_by_name}"; fi &&     existing_group_by_gid=`getent group "1000" | cut -f1 -d: || true` &&     if [ -z "${existing_group_by_gid}" ]; then       groupadd -g "1000" "ubuntu22";     fi &&     useradd --no-log-init --no-create-home --uid "1000" -s /bin/bash -c "ubuntu22,,," -g "1000" -d "/home/ubuntu22" "ubuntu22" &&     echo "ubuntu22 ALL=NOPASSWD: ALL" >> /etc/sudoers.d/rocker
building >  ---> Using cache
building >  ---> 50592c435e00
building > Step 10/12 : RUN mkdir -p "$(dirname "/home/ubuntu22")" && mkhomedir_helper ubuntu22
building >  ---> Using cache
building >  ---> 9f4a6ed0c2d5
building > Step 11/12 : USER ubuntu22
building >  ---> Using cache
building >  ---> 79b4cd678f00
building > Step 12/12 : WORKDIR /home/ubuntu22
building >  ---> Using cache
building >  ---> fd622b835fe8
building > Successfully built fd622b835fe8
Executing command: 
docker run --rm -it --name autoware_2  --network v2x_net   --gpus all --ip 10.0.0.3 --hostname autoware_2 --privileged -v /home/ubuntu22/autoware_main:/home/ubuntu22/autoware_main -v /home/ubuntu22/autoware_map:/home/ubuntu22/autoware_map  -e DISPLAY -e TERM   -e QT_X11_NO_MITSHM=1   -e XAUTHORITY=/tmp/.dockerjklrcqzo.xauth -v /tmp/.dockerjklrcqzo.xauth:/tmp/.dockerjklrcqzo.xauth   -v /tmp/.X11-unix:/tmp/.X11-unix   -v /etc/localtime:/etc/localtime:ro  fd622b835fe8 

```

并成功进入`autoware2`容器。如果未能成功，请见下一节解决方法。

### 2.1.4 安装Autoware docker镜像可能出现的问题及其解决方法

首先，上述命令行使用rocker工具构建容器，rocker工具是一种为构建docker容器加速的工具，autoware官方推荐使用，其逻辑为先在电脑本地查找有无autoware-universe:latest-cuda镜像，如果有，则直接从本地启动，如果没有，则从Dockerhub云端仓库下载。

如果本地已有镜像，那么使用`docker images`命令查看，应当有如下显示。

![image-20230818154925649](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308181549689.png)

**问题一：由于网络原因，下载不下来docker镜像，或者docker pull速度太慢。**在接近下载完成时要么失败，要么重新开始循环下载。

网络上常见的解决方法为：

![image-20230818164434466](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308181644504.png)

但是本人通过这种方法，实测没用，可能是因为近期服务商网络波动，加速网址被墙。因此国内的镜像代理加速通通不行，实测（阿里云，网易云，七牛云都没用）。



**解决方法：**

==通过docker proxy设置镜像代理，加快下载速度。==

详情见https://dockerproxy.com/网址教程，分为以下四个步骤。。

**第一步：**输入原始镜像地址获取命令.

```bash
ghcr.io/autowarefoundation/autoware-universe:latest-cuda
```

**第二步：**代理拉取镜像

```bash
docker pull ghcr.dockerproxy.com/autowarefoundation/autoware-universe:latest-cuda
```

**第三步：**重命名镜像

```bash
docker tag ghcr.dockerproxy.com/autowarefoundation/autoware-universe:latest-cuda ghcr.io/autowarefoundation/autoware-universe:latest-cuda
```

**第四步：**删除代理镜像

```bash
docker rmi ghcr.dockerproxy.com/autowarefoundation/autoware-universe:latest-cuda
```



本人是通过在笔记本电脑上通过`docker pull ghcr.dockerproxy.com/autowarefoundation/autoware-universe:latest-cuda`命令下载好镜像文件，然后将镜像打包成本地文件，拷贝至服务器电脑上安装成功。

下载完成后的步骤如下：

**1、将镜像打包成本地文件**
指令：docker save 镜像id > 文件名.tar

```bash
docker save 08edefe59662>./autoware_universe.tar	# autoware_universe.tar为打包的文件
```

**2、在另一台主机加载本地文件到镜像**

加载本地文件到镜像：
指令：docker load < 文件名.tar

```bash
docker load < autoware_universe.tar	  # autoware_universe.tar 为文件名称
```

**3、镜像重命名**

执行完上述语句后，查看本地镜像，会看到新加载的镜像名字和标签都是none，利用该镜像的id对名字和标签重新命名即可：
指令：docker tag 镜像id 镜像名:标签

```bash
docker tag 08edefe59662 ghcr.io/autowarefoundation/autoware-universe:latest-cuda
```



### 2.1.5 运行autoware规划仿真

在`autoware_1`和`autoware_2`中运行规划模拟器。

在`autoware_1`：

```bash
cd ~/autoware_main
source install/setup.bash
export AWID=1 # autoware_1
source /home/ubuntu22/autoware_main/src/v2x/autowarev2x/setup.sh
ros2 launch autoware_launch planning_simulator.launch.xml map_path:=/home/ubuntu22/autoware_map/sample-map-planning vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit
```

另外，在`autoware_1`中，通过单击`2D Pose Estimate`来设置自我车辆位置。

尝试通过单击`2D Dummy Car`添加一些虚拟汽车。请注意，您可以通过在`Tool Properties`窗格中将其`Velocity`更改为`0`来使虚拟汽车保持静态。

![img](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308141040960.png)

![img](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308141041770.png)

在`autoware_2`容器中：

```bash
cd ~/autoware_main
source install/setup.bash
export AWID=2 # autoware_2
source /home/ubuntu22/autoware_main/src/v2x/autowarev2x/setup.sh
ros2 launch autoware_launch planning_simulator.launch.xml map_path:=/home/ubuntu22/autoware_map/sample-map-planning vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit
```

### 2.1.6 运行 AutowareV2X模型

在另一个终端中，连接到`autoware_1`和`autoware_2`容器，并在这两个容器中启动 AutowareV2X。我们将`autoware_1`设置为 CPM 发送者，`autoware_2`设置为CPM 接收者。

在`autoware_1`：

```bash
docker exec -it autoware_1 bash  #进入正在运行中的容器
sudo su
cd ~/autoware_main
source install/setup.bash
export AWID=1
source ./src/v2x/autowarev2x/setup.sh
ros2 launch autoware_v2x v2x.launch.xml network_interface:=eth0
```



您应该看到如下所示的命令输出。它显示您正在“发送包含 n 个对象的 CPM”，并且该`[objectsList]`行描述了以下信息：`cpm_num, objectID, object.uuid, object.to_send, object.to_send_trigger`。 ![img](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308141040561.png)

在`autoware_2`：

```
docker exec -it autoware_2 bash
sudo su
cd workspace/autoware_docker
source install/setup.bash
export AWID=2
source ./src/v2x/autowarev2x/setup.sh
ros2 launch autoware_v2x v2x.launch.xml network_interface:=eth0 is_sender:=false
```



当发送器和接收器都启动时，您应该看到接收器 ( `autoware_2`) 将开始接收 CPM，如下所示。

![img](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308141040874.png)

### 2.1.7 Show CPM-shared objects in RViz 在 RViz 中显示 CPM 共享对象

1. Press "Add" from the Displays Panel

   从显示面板按“添加”

   ![img](https://tlab-wide.github.io/AutowareV2X/latest/tutorials/planning-simulation/add-v2x-rviz-1.png)

2. Choose "By topic", then select PredictedObjects from /v2x/cpm/objects

     选择“按主题”，然后从 /v2x/cpm/objects 中选择 PredictedObjects<br>![img](https://tlab-wide.github.io/AutowareV2X/latest/tutorials/planning-simulation/add-v2x-rviz-2.png)

3. The CPM-shared objects are shown in Rviz for `autoware_2`!

   CPM 共享对象显示在 `autoware_2`Rviz 中！<br>![img](https://tlab-wide.github.io/AutowareV2X/latest/tutorials/planning-simulation/add-v2x-rviz-3.png)

### 2.1.8 Run scenarios运行场景

In order to run scenarios, the [scenario_simulator_v2](https://github.com/tier4/scenario_simulator_v2.git) must be installed:

为了运行场景，必须安装[scene_simulator_v2 ：](https://github.com/tier4/scenario_simulator_v2.git)

1. Launch new Autoware container

   启动新的 Autoware 容器
```bash
rocker --nvidia --x11 --user --privileged --volume /home/ubuntu22/autoware_main --volume /home/ubuntu22/autoware_map --network=v2x_net --name autoware_1 --oyr-run-arg "--ip 10.0.0.2 --hostname autoware_1" -- ghcr.io/autowarefoundation/autoware-universe:latest-cuda
```
2. Add `simulator.repos`

   添加`simulator.repos`
```bash
cd workspace/autoware_docker
vcs import src < simulator.repos
```
3. Install dependent ROS packages

   安装依赖的ROS包
```bash
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -r
```
4. Rebuild workspace

   重编译工作区
```bash
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```
5. Download scenario.

   下载场景
```bash
gdown -O ~/data/scenarios/ 'https://drive.google.com/uc?id=1FXwSSWeFDTMz7qsG-J7pyJA6RgjksqCy'
```
6. Launch `scenario_test_runner` and specify scenario.

   启动`scenario_test_runner`并指定场景
```bash
ros2 launch scenario_test_runner scenario_test_runner.launch.py map_path:=/home/ubuntu22/autoware_map/sample-map-planning sensor_model:=sample_sensor_kit vehicle_model:=sample_vehicle scenario:=$HOME/data/scenarios/busy_kashiwa_scenario.yaml launch_autoware:=true
```

## 2.2 在实车中运行 AutowareV2X

待实验，实验完成后补充。

# 3. AutowareV2X代码研究

