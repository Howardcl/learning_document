# 1. 本地创建docker镜像

## 1.1 Docker镜像的创建方法

1. 基于已有镜像创建
2. 基于本地模板创建
3. 基于Dockerfile创建

### 阿里云镜像加速

1. 登录阿里云找到容器服务

   https://cr.console.aliyun.com/?spm=a2c4g.11186623.2.7.5daa7627kOSW0h

2. 2.找到镜像加速地址

![image](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308161200041.png)

3.配置使用

```shell
sudo mkdir -p /etc/docker
#创建一个目录
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://gbdey2h8.mirror.aliyuncs.com"]
}
EOF
#编写配置文件
sudo systemctl daemon-reload

sudo systemctl restart docker
```

![image](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308161200973.png)

> ## 回顾Hello World流程

![image](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308161200034.png)

![image](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308161445241.png)

### 底层原理

**Docker是怎么工作的？**

Docker是一个Client - Server结构的系统，Docker的守护进程运行在我们的主机上，通过Socket从客户端访问！

DockerServer接收到Docker-Client的指令，就会执行这个命令！

![image](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308161200648.png)

**Docker为什么比VM快**

1.Docker有着比虚拟机更少的抽象层。

2.Docker利用的是宿主机的内核，vm需要的是Guest OS

![image](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308161445272.png)

所以说，新建一个容器的时候，docker不需要像虚拟机一样重新加载一个操作系统内核，避免引导。虚拟机时加载Guest OS，分钟级别的，而docker是利用宿主机的操作系统，省略了复杂的过程，秒级的。

![image](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308161200867.png)

之后学习完所有的命令，再回过头来看这段理论，就会很清晰！

## 1.2 Docker的思想

```
集装箱：会将所有需要的内容放到不同的集装箱中，谁需要这些环境就直接拿到这个集装箱就可以了。

标准化：
运输的标准化：Docker有一个码头，所有上传的集装箱都放在了这个码头上，当谁需要某一个环境，就直接指派大海疼去搬运这个集装箱就可以了。
命令的标准化：Docker提供了一些列的命令，帮助我们去获取集装箱等等操作。
提供了REST的API：衍生出了很多的图形化界面，Rancher。
隔离性：Docker在运行集装箱内的内容时，会在Linux的内核中，单独的开辟一片空间，这片空间不会影响到其他程序。

中央仓库|注册中心：超级码头，上面放的就是集装箱

镜像：就是集装箱

容器：运行起来的镜像
```



## 1.3 Docker的常用命令

### 帮助命令

```shell
docker version      #显示docker的版本信息
docker info         #显示docker的系统信息，包括镜像和容器的数量
docker 命令 --help   #帮助命令
```

帮助文档的地址：https://docs.docker.com/reference/

### 镜像命令

docker images

```shell
[root@hsStudy ~]# docker images
REPOSITORY                TAG       IMAGE ID       CREATED         SIZE
hello-world               latest    d1165f221234   2 months ago    13.3kB
centos/mysql-57-centos7   latest    f83a2938370c   19 months ago   452MB
# 解释
REPOSITORY 镜像的仓库源
TAG        镜像的标签
IMAGE ID   镜像的创建时间
SIZE       镜像的大小

#可选项
Options:
  -a, --all             # 列出所有的镜像
  -q, --quiet           # 只显示镜像的ID
```

**docker search搜索镜像**

```shell
[root@hsStudy ~]# docker search mysql
NAME                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
mysql                             MySQL is a widely used, open-source relation…   10881     [OK]
mariadb                           MariaDB Server is a high performing open sou…   4104      [OK]       

# 可选项，通过收藏来过滤
--filter=STARS=3000  搜索出来的镜像就是STARS大于3000的
```

**docker pull 下载命令**

```shell
#下载镜像 docker pull 镜像名[:tag]
[root@hsStudy ~]# docker pull mysql
Using default tag: latest   #如果不写tag，默认就是latest
latest: Pulling from library/mysql
69692152171a: Pull complete #分层下载，docker images核心 联合文件地址
1651b0be3df3: Pull complete 
951da7386bc8: Pull complete 
0f86c95aa242: Pull complete 
37ba2d8bd4fe: Pull complete 
6d278bb05e94: Pull complete 
497efbd93a3e: Pull complete 
f7fddf10c2c2: Pull complete 
16415d159dfb: Pull complete 
0e530ffc6b73: Pull complete 
b0a4a1a77178: Pull complete 
cd90f92aa9ef: Pull complete 
Digest: sha256:d50098d7fcb25b1fcb24e2d3247cae3fc55815d64fec640dc395840f8fa80969
Status: Downloaded newer image for mysql:latest
docker.io/library/mysql:latest #真实地址

# 等价于
docker pull mysql
docker pull docker.io/library/mysql:latest

# 指定版本下载
[root@hsStudy ~]# docker pull mysql:5.7 
5.7: Pulling from library/mysql
69692152171a: Already exists 
1651b0be3df3: Already exists 
951da7386bc8: Already exists 
0f86c95aa242: Already exists 
37ba2d8bd4fe: Already exists 
6d278bb05e94: Already exists 
497efbd93a3e: Already exists 
a023ae82eef5: Pull complete 
e76c35f20ee7: Pull complete 
e887524d2ef9: Pull complete 
ccb65627e1c3: Pull complete 
Digest: sha256:a682e3c78fc5bd941e9db080b4796c75f69a28a8cad65677c23f7a9f18ba21fa
Status: Downloaded newer image for mysql:5.7
docker.io/library/mysql:5.7
```

![image](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/202308161331939.png)

dockers rml 删除镜像

```shell
[root@hsStudy ~]# docker rmi -f 镜像id #删除指定的镜像
[root@hsStudy ~]# docker rmi -f 镜像id 容器id 容器id #删除多个指定的镜像
[root@hsStudy ~]# docker rmi -f $(docker images -aq) # 删除全部镜像
```

### **容器命令**

**说明：我们有了镜像才可以创建容器，linux，下载一个CentOS镜像来测试学习**

```shell
docker pull centos
```

**新建容器并启动**

```shell
docker run [可选参数] image

#参数说明
--name="Name"   容器名字  tomcat01  tomcat02 用来区分容器
-d              以后台方式运行，ja nohub
-it             使用交互模式运行，进入容器查看内容
-p              指定容器的端口 -p 8080:8080
	-p ip主机端:容器端口
	-p 主机端:容器端口   主机端口映射到容器端口 （常用）
	-p 容器端口
	容器端口
	
-P              随机指定端口

#测试，启动并进入容器
[root@hsStudy ~]# docker run -it centos /bin/bash
[root@9f8cb921299a /]#
[root@9f8cb921299a /]# ls #查看容器内的centos，基础命令很多都是不完善的
bin  etc   lib	  lost+found  mnt  proc  run   srv  tmp  var
dev  home  lib64  media       opt  root  sbin  sys  usr

#从容器中退回主机
[root@9f8cb921299a /]# exit
exit
[root@hsStudy /]# ls
bin   dev  home  lib64       media  opt   root  sbin  sys  usr
boot  etc  lib   lost+found  mnt    proc  run   srv   tmp  var
```

**列出所有运行中的容器**

```shell
# docker ps 命令
	 #列出当前正在运行的容器
-a   #列出当前正在运行的容器+带出历史运行过的容器
-n=? #显示最近创建的容器
-q   #只显示容器的编号

[root@hsStudy ~]# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
[root@hsStudy ~]# docker ps -a
CONTAINER ID   IMAGE          COMMAND       CREATED         STATUS                     PORTS     NAMES
9f8cb921299a   centos         "/bin/bash"   7 minutes ago   Exited (0) 4 minutes ago             eager_keldysh
da964ff44c74   d1165f221234   "/hello"      6 hours ago     Exited (0) 6 hours ago               affectionate_shtern
```

**退出容器**

```shell
exit  #直接让容器停止并退出
Ctrl + P + Q #容器不停止退出
[root@hsStudy ~]# docker ps 
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
[root@hsStudy ~]# docker run -it centos /bin/bash
[root@49bbf686f9a3 /]# [root@hsStudy ~]# docker ps 
CONTAINER ID   IMAGE     COMMAND       CREATED          STATUS          PORTS     NAMES
49bbf686f9a3   centos    "/bin/bash"   14 seconds ago   Up 12 seconds             sharp_kilby
[root@hsStudy ~]# 
```

**删除容器**

```shell
docker rm 容器id                 #删除指定的容器，不能删除正在运行的容器，如果要强制删除，rm -f
docker rm -f $(docker ps -aq)   #删除所有的容器
docker ps -a -q|xargs docker rm #删除若有容器（使用linux管道命令）
```

**启动和停止容器的操作**

```shell
docker start 容器id     #启动容器
docker restart 容器id   #重起容器
docker stop 容器id      #停止当前正在运行的容器
docker kill 容器id      #强制停止当前容器
```

### 常用其他命令

**后台启动容器**

```shell
# 命令 docker run -d 镜像名
[root@hsStudy ~]# docker run -d centos


# docker ps ， 发现centos停止了

# 常见的坑，docker 容器使用后台运行，就必须要有一个前台进程，docker发现没有应用，就会自动停止
#nagix，容器启动后，发现自己没有提供服务，就会立即停止，没有程序了 
```

**查看日志命令**

```shell
docker logs -f -t --tail 容器 没有日志

# 自己编写一段shell脚本
[root@hsStudy /]# docker run -d centos /bin/sh -c "while true;do echo hansuo;sleep;done"

[root@hsStudy /]# docker ps
CONTAINER ID   IMAGE     
4466628037e0   centos   

#显示日志
-tf           #显示日志
--tail number # 要显示的日志条数
docker logs -f -t --tail 10 4466628037e0
```

**查看容器中的进程信息**

```shell
# 命令 docker top 容器id
[root@hsStudy /]# docker top 4466628037e0
UID                 PID                 PPID                C                   STIME               TTY     
root                9218                9198                10                  15:47               ?       
```

**进去当前正在运行的容器**

```shell
# 我们通常容器都是是同后台方式进行的，修改一些配置

#命令
docker exec -it 容器id bashShell

#测试
[root@hsStudy /]# docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS     NAMES
4466628037e0   centos    "/bin/sh -c 'while t…"   16 minutes ago   Up 16 minutes             blissful_bhaskara
[root@hsStudy /]# docker exec -it 4466628037e0 /bin/bash
[root@4466628037e0 /]# ls
bin  etc   lib	  lost+found  mnt  proc  run   srv  tmp  var
dev  home  lib64  media       opt  root  sbin  sys  usr
[root@4466628037e0 /]# ps -ef
UID         PID   PPID  C STIME TTY          TIME CMD
root          1      0 10 07:47 ?        00:02:01 /bin/sh -c while true;do echo hansuo;sleep;done
root      49735      0  0 08:05 pts/0    00:00:00 /bin/bash
root      51738  49735  5 08:05 pts/0    00:00:00 ps -ef
root      51745      1  0 08:05 ?        00:00:00 [sh]

#方式二
docker attach 容器id
#测试
[root@hsStudy /]# docker attach 4466628037e0
正在执行当前的代码...

#decker exec     #进入容器后开启一个新的终端，可以在里面操作（常用）
#docker attach   #进入容器正在执行的终端，不会启动新的进程！
```

**从容器内拷贝文件到主机上**

```shell
docker cp 容器id:容器内路径 目的的主机

#查看当前主机目录下
[root@hsStudy home]# ls
depp  hansuo.java
[root@hsStudy home]# docker ps
CONTAINER ID   IMAGE     COMMAND       CREATED         STATUS         PORTS     NAMES
afb3e7611084   centos    "/bin/bash"   3 minutes ago   Up 3 minutes             epic_galileo

#进入docker容器内部
[root@hsStudy home]# docker attach afb3e7611084
[root@afb3e7611084 /]# cd /home
[root@afb3e7611084 home]# ls

#在容器内新建一个文件
[root@afb3e7611084 home]# touch test.java
[root@afb3e7611084 home]# ls
test.java
[root@afb3e7611084 home]# exit
exit
[root@hsStudy home]# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
[root@hsStudy home]# docker ps -a
CONTAINER ID   IMAGE     COMMAND       CREATED         STATUS                     PORTS     NAMES
afb3e7611084   centos    "/bin/bash"   5 minutes ago   Exited (0) 8 seconds ago             epic_galileo

#将这个文件拷贝出来到我们的主机上
[root@hsStudy home]# docker cp afb3e7611084:/home/test.java /home
[root@hsStudy home]# ls
depp  hansuo.java  test.java
[root@hsStudy home]# 

#拷贝是一个手动过程，未来我们使用 -v 卷的技术可以实现，自动同步 /home
```

# 2. Docker 手动拉取镜像到本地节点

在使用 Docker 进行容器化部署时，我们通常需要从 Docker 镜像仓库中拉取所需的镜像。然而，有时候由于网络问题或其他原因，我们可能无法直接从镜像仓库中拉取镜像。为了解决这个问题，我们可以手动拉取镜像到本地节点，然后再使用这个本地镜像进行容器的创建和运行。

#### 什么是 Docker 镜像

Docker 镜像是用于创建 Docker 容器的模板。它包含了运行容器所需的文件系统、软件环境和配置信息。

Docker 镜像是通过 Dockerfile 来构建的。一个 Dockerfile 文件中包含了一系列的指令，用于指定如何构建镜像。这些指令可以包括从基础镜像构建、复制文件、运行命令等。

#### Docker 镜像仓库

Docker 镜像仓库是存放 Docker 镜像的地方。我们可以通过 Docker 镜像仓库来获取所需的镜像，并在本地节点上使用。

Docker 官方提供了一个公共的 Docker 镜像仓库，称为 Docker Hub。Docker Hub 中包含了大量的官方和社区维护的镜像，供开发者使用。

除了 Docker Hub，还有其他的 Docker 镜像仓库可供选择，比如阿里云容器镜像服务、腾讯云镜像仓库等。

#### 手动拉取镜像到本地节点

当无法直接从 Docker 镜像仓库中拉取镜像时，我们可以将镜像手动下载到本地节点，并导入到 Docker 中。

以下是手动拉取并导入镜像的步骤：

在能够访问 Docker 镜像仓库的机器上，使用 docker pull 命令下载所需的镜像。

```
$ docker pull <镜像名称>:<标签>
```



在下载完成后，使用 docker save 命令将镜像保存为 tar 文件。

```
$ docker save -o <保存路径>/<镜像名称>.tar <镜像名称>:<标签>
```



将 tar 文件拷贝到目标机器上。

在目标机器上使用 docker load 命令导入镜像。

```
$ docker load -i <保存路径>/<镜像名称>.tar
```



完成以上步骤后，镜像就被成功导入到了目标机器的 Docker 中。

注意：手动导入的镜像没有经过验证和验证签名，因此需要确保从可信任的来源获取镜像文件。

#### 示例

以下是一个手动拉取镜像到本地节点的示例：

下载 Ubuntu 18.04 镜像

```
$ docker pull ubuntu:18.04

保存镜像为 tar 文件
$ docker save -o /tmp/ubuntu_18.04.tar ubuntu:18.04
```



```
将 tar 文件拷贝到目标机器上
$ scp /tmp/ubuntu_18.04.tar <目标机器>:<保存路径>

在目标机器上导入镜像
$ docker load -i <保存路径>/ubuntu_18.04.tar

```

这样，我们就成功地将 Ubuntu 18.04 镜像手动拉取到了本地节点，并可以在目标机器上使用该镜像进行容器的创建和运行了。

在实际应用中，我们可以根据需要手动拉取任意镜像到本地节点，以满足容器化部署的需求。

### 镜像的操作【重点】

5.1 拉取镜像
从中央仓库拉取镜像到本地

```
docker pull 镜像名称[:tag]

### 举个栗子：docker pull daocloud.io/library/tomcat:8.5.15-jre8
```



5.2 查看本地全部镜像
查看本地已经安装过的镜像信息，包含标识，名称，版本，更新时间，大小

```
docker images
```



5.3 删除本地镜像
镜像会占用磁盘空间，可以直接手动删除，表示通过查看获取,注意被删除的镜像一定不存在容器。

```
docker rmi 镜像的标识
```



5.4 镜像的导入导出
如果因为网络原因可以通过硬盘的方式传输镜像，虽然不规范，但是有效，但是这种方式导出的镜像名称和版本都是null，需要手动修改

### 将本地的镜像导出

docker save -o 导出的路径 镜像id

### 加载本地的镜像文件

```
docker load -i 镜像文件
```



### 修改镜像名称

```
# 将本地的镜像导出
docker save -o 导出的路径 镜像id
# 加载本地的镜像文件
docker load -i 镜像文件
# 修改镜像名称
docker tag 镜像id 新镜像名称:版本
```

