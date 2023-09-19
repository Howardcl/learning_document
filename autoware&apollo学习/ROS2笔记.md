**1.**概述

​     ROS2提供了一套非常丰富的服务质量(Quality of Service, **QoS**)策略用于调整节点之间的通信。众所周知，在TCP与UDP之间存在着无数的折中设置，QoS既可以设置成像TCP一样可靠(reliable)，也可以设置成像UDP一样高效(best effort)。不同于ROS1，它主要支持TCP通信，ROS2底层采用的是DDS(Data Distribution Service)传输，当DDS工作在损无线网络(lossy wireless network)中时更有利于best-effect策略，当DDS工作在实时计算系统中时通过设置适合的QoS策略来满足实时性。

一套QoS策略形成了一个QoS Profile。考虑到为特定的场景选择正确QoS策略较为复杂，ROS2提供了一套预定义的QoS Profiles，用于常见场景(如传感器数据)。同时，也提供了特定的Profiles给使用者设置QoS策略。

发布器、订阅器、服务端和客户端可以指定Profile，且它们的每个实例都可以单独指定Profile，但不兼容的Profiles可能导致无法通信。

**2.QoS****策略**

​     当前，QoS Profile提供了对以下QoS策略的设置：

​     **(1)****历史记录****(History)**

​     保留近期记录(**Keep last**)：缓存最多N条记录，可通过队列长度选项来配置。

​     保留所有记录(**Keep all**)：缓存所有记录，但受限于底层中间件可配置的最大资源。

​     **(2)****深度****(Depth)**

​     队列深度(Size of the queue)：只能与Keep last配合使用。

​     **(3)****可靠性****(Reliability)**

​     尽力的(**Best effort**)：尝试传输数据但不保证成功传输(当网络不稳定时可能丢失数据)。

​     可靠的(**Reliable**)：反复重传以保证数据成功传输。

​     **(4)****持续性****(Durability)**

​     局部瞬态(**Transient local**)：发布器为晚连接(late-joining)的订阅器保留数据。

​     易变态(**Volatile**)：不保留任何数据。

​     以上每个策略都有系统默认值。这个默认值就是底层中间件的默认值，由DDS供应商工具(如XML配置文件)定义。DDS本身提供了许多可配置的策略。这些策略与ROS1的特征相似，所以在ROS1中是可见的。之后可能会有更多的策略在ROS2中可见。

**3.****与****ROS1****的比较**

​     ROS2的History和Depth结合起来类似于ROS1的队列大小功能。

​     ROS2的Reliability取Best-effort类似于ROS1的UDPROS(仅roscpp包含此功能)，取Reliable类似于ROS1的TCPROS。

​     ROS2的Durability和队列深度为1的Depth结合起来类似于ROS1中的latching订阅器。

**4.QoS****配置文件**

​     Profile使开发者专注于他们的应用，而无需担心QoS的各种设置。一个QoS Profile包含一套策略，可以高效地配合特定的用例工作。当前定义了一些默认的Profiles，以下对它们进行介绍。

​     **(1)****默认**(qos_profiles.h：rmw_qos_profile_system_default)

​     所有的策略设置为RMW的默认值。不同的RMW默认值可能存在差异。

​     **(2)****主题**(qos_profiles.h：rmw_qos_profile_default)

​     为了保证ROS1和ROS2之间的过渡，有必要设计一套相似的网络行为。于是，设置发布器和订阅器的默认Profile为(Keep last, 10, Reliable, Volatile)。

​     **(3)****服务**(qos_profiles.h：rmw_qos_profile_services_default)

​     与发布器和订阅者器一样，服务首先得reliable。其次，Volatile对服务也是必须的，否则会收到过时的请求。尽管客户端已被设计避免接收多次响应，但服务端没有设计如何处理过时的请求产生的副作用。服务Profile的详细取值为(Keep last, 10, Reliable, Volatile)。

​     **(4)****参数**(qos_profiles.h：rmw_qos_profile_parameters)

​     参数是基于服务的，所以有相似的Profile。不同之处参数具有更大的队列深度，以避免丢失请求(例如当在参数客户端不能访问参数服务端时)。参数Profile的详细取值为(Keep last, 1000, Reliable, Volatile)。

​     **(5)****参数事件**(qos_profiles.h：rmw_qos_profile_parameter_events)

与参数Profile相同。

​     **(6)****传感器数据**(qos_profiles.h：rmw_qos_profile_sensor_data)

​     在大多数用例中，需要实时读取传感器的数据而无需读取所有数据。也就是说，开发者希望尽快地获取最新数据，为此可以丢失一些数据。因此，传感器需要Best effort和更小的队列深度，其Profile详细取值为(Keep last, 5, Best effort, Volatile)。

​     以上Profiles更多信息可参见~\ros2\include\rmw\qos_profiles.h。这些Profiles的取值会根据社区的反馈意见进一步的调整

​     虽然ROS2提供了一些常用的QoS Profiles，但DDS中定义的策略允许ROS用户基于现有的DDS文档提供的大量的信息来为其特定的用例设置QoS Profile。

**5.QoS****兼容性**

​     注意：以下内容以发布器和订阅器举例阐述，但同样适合于服务端和客户端。

​     发布器和订阅器可以分别指定自己的OoS Profiles。只有当它们的Profiles兼容时，两者才能建立连接。Profile的兼容性基于"请求与提供"(Request vs Offerer)模型，只有当订阅器的策略没有发布器的严格时，连接才能建立，且建立的连接使用严格度低的策略。

​     ROS2中存在兼容性问题的OoS策略是Durability和Reliability。下面的展示了不同策略配置的兼容性结果：

**Durability****的兼容性配置：**

| **Publisher**   | **Subscriber**  | **Connection** | **Result**      |
| --------------- | --------------- | -------------- | --------------- |
| Volatile        | Volatile        | Yes            | Volatile        |
| Volatile        | Transient local | No             |                 |
| Transient local | Volatile        | Yes            | Volatile        |
| Transient local | Transient local | Yes            | Transient local |

**Reliability****的兼容性配置：**

| **Publisher** | **Subscriber** | **Connection** | **Result**  |
| ------------- | -------------- | -------------- | ----------- |
| Best effort   | Best effort    | Yes            | Best effort |
| Best effort   | Reliable       | No             |             |
| Reliable      | Best effort    | Yes            | Best effort |
| Reliable      | Reliable       | Yes            | Reliable    |
