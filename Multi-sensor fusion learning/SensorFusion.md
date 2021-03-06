Combining two or more data sources in a way that generates a better understanding of the system.  这里“更好”指的是：比单一数据源更具有一致性（more consistent），更精确（more accurate），更可靠（more dependable）。

![image-20210323183519577](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210323183519.png)

多数情况下，认为数据是来自传感器的，它所测量的数据提供了对系统的理解。这些数据例如加速度，或者与某个目标之间的距离。

自动系统需要具备四个功能：传感、感知、计划和执行。

- 传感：measuring the environment with sensors, collecting information from the system and the external word.

  从系统和外部世界收集信息，为自动驾驶汽车提供信息，例如这个传感器套件可能包括雷达、激光雷达、摄像头等。但仅仅用传感器收集信息是不够的，因为系统需要解释数据，并转化为系统能够理解和执行的东西，这一步就是感知的作用。

- 感知：赋予传感数据意义。这一步负责自我意识(`self-awareness`)，比如自我定位；还要负责姿态感知(`situational awareness`)，比如探测环境中的其他物体并跟踪它们。

- 计划：确定自己想做什么，并找到一条实现目标的途径。

- 执行：计算出遵循这条路径的最佳操作，这一步需要控制器。

![image-20210323185741840](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210323185741.png)

那么`data fusion`的作用是啥？

它能够跨传感和感知工作。这个过程中会获取多个传感器的测量值，将其进行组合，并混合数学模型中的附加信息。

（1）可以提高数据的质量（It can increase the quality of the data）我们始终希望使用的数据噪声少，不确定性小，与真实值偏差小。

比如说将单个加速度计放在静止的桌子上，测量重力加速度。如果这是一个完美的传感器，输出读书将为常数`9.81 m/s²`。然而实际测量会有噪声，噪声的大小取决于传感器的质量，这是不可预测的噪声（the actual measurement will be noisy, how noisy depends on the quality of the sensor and this is unpredictable）,因此我们无法通过校准来消除它，只能通过添加第二个加速度计，对两个读数取平均值，则可以降低信号中的总噪声．

只要传感器之间的噪声不相关，就可以将它们融合在一起，这样可以将组合噪声降低为传感器数量平方根的几分之一，所以四个完全相同的传感器融合在一起的组合噪声只有单个传感器噪声的一半．这个非常简单的传感器融合算法就是求平均的函数．我们还可以通过组合来自两个或更多不同类型传感器的测量值来减少噪声．

![image-20210323191030814](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210323191030.png)

卡尔曼滤波器是比较通用的方法之一。

（2）增加测量的可靠性(It can increase reliability)．

一个传感器的故障虽然可能会降低系统数据的质量，但不会损失整个测量结果。还可以引入第三个传感器，将产生了不同于其他两个测量值的任何单个传感器的数据剔除掉。

（3）可以预测不可测量的状态(It can estimate unmeasured states). 

单个相机不能测量距离，但两个相机的组合可以测量三个维度．可以测量两幅图像中目标之间的相对距离. 

总之，使用多个数据源可以提高测量质量，可靠性和覆盖范围，并能估算出不能直接测量的状态值．



**Single model estimation filter (often a kalman filter)  =>  Interacting multiple model filter (IMM)**

`IMM`是解决跟踪问题的一种非常不错的方法。那么当跟踪一个不确定的目标时，`IMM`如何实现状态的估计（预测）？

跟踪机动目标（Tracking Maneuvering Targets）的示例：

https://ww2.mathworks.cn/help/fusion/ug/tracking-maneuvering-targets.html

`IMM`在跟踪机动目标时效果更好，通过所有三个机动的归一化距离比比单模型滤波器低得多，为什么呢，是什么让`IMM`如此特别？

![image-20210324113446572](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324113448.png)

预测滤波器（比如卡尔曼滤波器）的工作原理是：预测系统的未来状态，然后通过测量来校正该状态。因此我们先预测，后再进行测量和校正。为了进行预测，我们必须为滤波器提供一个系统模型，它可以用来预测将来某个时刻系统的位置。然后在将来的某个时刻，使用一个或多个传感器对系统状态进行测量，然后使用该测量状态基于对状态和预测的相对置信度来校正预测状态，该混合结果是滤波器的输出。

![image-20210324143419979](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324143420.png)

![image-20210324143743984](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324143744.png)

单一模型滤波器对匀速运动比较适用，但在转弯和有加速度的情况下效果不好。因此我们应该通过增加滤波器中的过程噪声来解决这一点，减少对预测的置信度，相应地增加对修正观测值的置信度。当很难预测目标的位置时，为什么不相信观测结果而忽略大部分无用的预测呢？

![image-20210324144756234](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324144756.png)

增加过程噪声后，在目标转弯和加速时，预测结果得到了改善，但这也是有代价的，匀速运动阶段的结果变糟了，因为我们更多地依赖于噪声测量。所以如果不能相信预测且主要依赖于传感器的观测值，那么该预测滤波器有什么用呢？重点是使用预测来解决一些测量噪声，从而降低总体不确定性。

![image-20210324144922137](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324144922.png)

与仅仅使用传感器测量目标相比，我们如何能够更好地预测机动目标的状态？答案就是运行多个模型。基本上可以认为这是运行几个同步预测滤波器，每个滤波器具有不同的预测模型和过程噪声。这样做的目的是希望跟踪目标参与的每种运动类型建立一个模型，包括匀速运动，匀加速运动和恒定转动等覆盖所有可能运动的类型。每种模型都能预测目标的运动方向（如果该目标遵循特定的运动模式）。然后，当我们得到一个测量值时，会将这个测量值与每种模型所得到的预测值进行比较。由此，我们可以推断出哪个模型最可能代表目标真实的运动，我们可以在下一个预测周期对该模型给予更多的信任。

![image-20210324151518725](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324151518.png)

这就像人做预测一样，如果目标看起来是直线运动，我们就会假设它将保持直线飞行，如果看到它开始转向，就会假设转弯将持续一段时间，利用这种方法，当目标转换为一个新的运动类型时会出现一些瞬时误差，但是滤波器会很快意识到新模型具有很好的预测，并会开始增加其可能性。这就是多个模型算法背后一般的思想，但是要实现多个模型的交互，还有一个步骤。

但会遇到一个问题，每个滤波器都是独立运行的，与其他目标向隔离，这意味着对于一个不能代表真实运动的模型，将保持对系统状态和状态协方差的错误预测。然后，当目标运动发生变化并且存在向该模型的转换时，由于其不良的状态预测和协方差，滤波器需要一段时间才能再次收敛。因此，通过这种方式，每次过渡到新的运动时，在滤波器试图跟进期间过渡时间将比必需的长。要解决此问题，我们允许模型进行交互，测量之后整体滤波器会根据最可能的模型的混合获得最新的状态和状态协方差。此时，每个滤波器都会根据状态和协方差的切换或混合的概率进行重新初始化。这将不断改进每个滤波器，以减少其自身的残余误差，即使在它不代表目标的真实运动时也是如此。通过这种方式，`IMM`滤波器可以切换到单个模型，而不必等待其先收敛，该模型之所以效果好是因为由三个模型组成：匀速、转弯和加速度，以匹配目标的三个预期运动。

![image-20210324151933841](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324151933.png)

上图中，右上角是目标的机动曲线图，右下角有三种不同的颜色，显示了`IMM`中每个模型代表真实运动的可能性。可以看到使用`IMM`模型时，三种机动的总归一化距离都很小，在目标进行其预测的运动并且运动之间的瞬态时间很短，查看一下每个模型的可能性是如何飙升的。因此只要目标不是持续快速地改变运动，那么此瞬态误差就不会对预测的整体质量产生太大影响。这就是在跟踪不协作目标时弥补控制输入信息不足的方法。我们为每个预期的运动建立一个模型，然后创建`IMM`以根据它们代表真实运动的可能性将它们融合在一起。

![image-20210324152741133](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324152741.png)

为什么不运行一个包含一百万个模型的`IMM`，这样不就几乎包含了所有可能的运动吗？一是模型太多需要太大的计算资源，降低了计算速度；二是降低了性能，因为它增加了模型之间的转换次数，如果有很多模型代表非常相似的运动，那么就很难确定何时应该进行转换，这两个而因素都会导致预测效果较差。因此，就必须以一种智能的方式使用滤波器，并尝试找到可以充分预测所跟踪目标的可能运动的最小的模型集合。实际上，这往往会少于10个模型，通常只有3个或者4个。另外要记住一点，以上都仅仅是跟踪单个目标的必要条件。当我们扩展到同时跟踪多个目标时，问题会变得更加棘手。

使用滤波器算法改善对机动目标的跟踪：（CV不加噪声、CV加噪声、IMM）

https://ww2.mathworks.cn/help/fusion/ug/tracking-maneuvering-targets.html



只采用`IMM`跟踪算法将其应用于每个目标，就可以跟踪多个目标了吗？当然不能，还需要考虑其他的一些问题。

![image-20210324154242793](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324154242.png)

当然仅仅靠一种算法不能解决问题，因为每个问题都是不同的，目标有多少，可以访问不同的测量数据和信息，或者对目标之间的距离有不同的期望值，目标是稀疏分布的还是杂乱分布的，使用的计算资源不同，需要的准确度有不同的需要等等。如何弄清楚要解决的特定问题更像是一门艺术。通过学习再进行选择和开发。

![image-20210324154403461](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324154403.png)

为什么多目标跟踪困难？因为**不确定性**。这是对目标的观测的不确定性，以及我们对目标所走路径的预测的不确定性。卡尔曼滤波器这样的滤波器就是通过混合不确定的测量值和不确定的预测值进行工作的。比如说用雷达跟踪飞机，我们预测了飞机未来的位置，并用噪声雷达测量值进行校正。但我们有很多目标，而不是一个单一目标，每个目标都有自己的不确定预测值，我们需要用其相应的不确定测量值进行校正。

那么就引出了第一个问题，我们不想用另一个目标的测量值来修正对某个目标的预测。但如果检测过程中没有识别信息，比如飞机尾号或者其他一些独特的特征，我们如何知道我们刚刚检测到的是哪个目标？我们如何将任意的观测值与相应的跟踪目标进行匹配？

如果所有目标都是稀疏分布的，并且观测结果相对可靠，这并不是什么大问题，获得最接近的目标的观测值很简单。这种情况下，我们只需要将测量值分配给最近的目标，像跟踪单个目标一样运行估计滤波器。

![image-20210324155709903](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325210551.png)

但如果目标之间距离很近或者观测值的不确定性很大时，以至于测量目标可能不止一个，问题就变得棘手起来。此时必须将检测结果与正确的目标相关联，需要做的工作是**数据关联问题(Data association problem)**。

![image-20210324155912645](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324155912.png)

另一个问题是：被跟踪目标的数量不是固定的，有时需要根据我们的观察来创建或者删除轨迹。当目标进入检测范围时，需要添加一条新的轨迹，当目标离开检测范围时，需要删除这个目标的轨迹。

![image-20210324160059542](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324160059.png)

轨迹的创建和删除不仅发生在传感器`FOV(the Field of View)`的边缘．可能在任何地方创建和删除，需要考虑创建和删除目标轨迹的标准，解决该问题的一种基本办法是：只要检测到与现有目标不匹配的情况就添加一条新的轨迹，如果未检测到现有目标就删除一条轨迹。

让事情复杂化的是，有时传感器会产生误报。发现的目标可能实际并不存在，或者实际存在的目标没有检测到。所以需要格外注意，以免过早地创建轨迹，因为这样会扰乱我们对实际存在目标的看法；并且要避免过早地删除轨迹，这样会降低跟踪效率。这就是**轨迹维护问题(track maintenance problem)**。

![image-20210324161012951](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324161013.png)

**当跟踪多个目标时，如何处理数据关联问题和轨迹维护问题?**

流程图:

![image-20210324161105495](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324161105.png)

**第一步：观测（observation）**

目标观测值可能包括距离，距离变化率，这些数值表示目标的运动学性质，也可能包含测量的属性，例如目标的类型，目标的`ID`或者目标的形状。

![image-20210324161231204](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324161231.png)

观测需要考虑的其他事项是，如果跟踪的目标是点目标(Point target)，则观测最多将包含一个检测结果(detection)，因此必须将一个检测结果与一个目标相关联。如果目标很大，且传感器具有足够的分辨率，每个目标可能有不止一个检测结果，在确定如何处理这种数据的关联时，需要考虑一点。如果在一次检测中存在两个目标，这种情况下，我们已经观察到两个目标，因此我们不想停止跟踪它们中的任何一个，但是它们只会显示为一次检测 (only show a single detection)，我们的轨迹删除算法必须解决这种问题。

![image-20210324161848301](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324161848.png)

下面只讨论每个被跟踪目标进行一次检测的情况，并且将在第二步的分配工作中处理这个问题。

**第二步，分配（assignment）**

分配时将观测结果与被跟踪目标相关联的过程，也就是将其与轨迹相匹配（Matching an observation to a tracked object / a track）。最简单的分配算法(assignment algorithm)是**`GNN`**，即**`（Global Nearest Neighbor）`全局最邻近**，只需为最近的观测点指定一个轨迹，但有趣的是这个"最近"未必是欧几里德距离或者几何距离最近，而是最近的概率距离，就像用马氏距离`(Mahalanobis distance)`测得的一样。

原因是，对于概率分布，就像对于预测和测量一样，最小的欧几里得距离并不总是表示预测和测量是最佳拟合，这是因为我们对标准偏差较小方向上的预测和测量更有信心。比如说在下图中，我们预测了两个不同物体的位置，并在它们之间进行了一次检测，如果我们使用欧几里得距离，我们会假设检测到的是目标２，因为目标2离观测值更近，但如果我们看一下这两种预测的概率分布，可以发现检测到的目标１的可能性更大，这就是马氏距离对我们的影响，它是通过标准差归一化的距离。`GNN`对于稀疏分布的目标(sparsely distributed object)效果很好，但对于杂乱分布的目标 —— `JPDA（Joint probabilistic data association algorithm）`，也成为联合概率数据关联算法更有效果。

![image-20210324162626672](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324162626.png)

`JPDA`不会在一个观测值和一个轨迹之间进行硬匹配，相反，它会将所有相邻观测值进行加权组合，距离较近的观测值的加权值高于其他观测值，这是对`GNN`的一个改进。因为如果有两个观测值可能会成为目标，那么`JPDA`不会完全专注于某一个，因为这个目标也许是错误的。如果被跟踪的目标彼此靠近，并且观测值也都在其附近聚集，则该算法可以通过将一些目标混合在一起来解决问题，而不必在错误的观测值与正确的观测值之间来回切换。

![image-20210324163019947](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324163020.png)

分配算还有很多，可以根据自己的跟踪情况创建自己的算法，但最重要的是，你需要尝试找出如何将观测值与轨迹相关联。不是所有的观测值都会被分配，也不是所有的轨迹都有观测值，此时就需要轨迹维护，它通常采用删除和创建轨迹的形式。但必须小心，以免过早做出任何决策。

**第三步，轨迹维护（track maintenance）**

首先从一种保守的删除轨迹的方法开始，我们不会因为一个目标错过一次观测就认定其消失了，我们只会在最近的`R`次更新中，至少有`P`次没有将轨迹分配给观测值时才会删除该轨迹。其中，`P`和`R`是可以根据自己的情况进行调整的参数。比如，如果在最近的6次更新中至少有4次没有检测到某个轨迹，就可以认定该轨迹已经离开检测范围了，可以将该轨迹给删除了。

![image-20210324163326419](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324163326.png)

现在，创建轨迹有点棘手，因为不知道单个未分配的观测值是否会立即成为新的目标，但是仍然需要注意，以便随着时间的推移找出是否值得跟踪。解决这个问题的一种方法是创建一条**暂留轨迹**，你可以将其维护并假定为真实目标，但实际上并不认为这是真实目标，你只需要在后台维护该轨迹即可。如果在最近的`N`次更新中`M`次检测到该暂定轨迹，就可以将其移到**已确定轨迹**中去，这意味着认为它是真实目标。可以使用与删除已确认轨迹相同的逻辑删除暂定轨迹。因此，在这种情况下，由于误报观测值，可能要维护数十条暂定轨迹，但在确认之前需要将其删除。

![image-20210324163530667](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324163530.png)

创建和删除轨迹并分配观测值后，可以运行一组估计滤波器，这部分与单个目标的跟踪相同。

**第四，估计滤波器（estimation filter）**

可以在其中选择交互多模型滤波器`IMM`或者单模型卡尔曼滤波器。分配了观测值的每个跟踪目标（暂留目标和已确认目标）的预测状态都将使用其各自的观测值进行更新，然后整个过程重新开始。我们将得到更多的观测值，观测值会分配给轨迹，轨迹将被创建和删除，然后滤波器再次运行。

![image-20210324164001484](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324164001.png)

第五步：门控（Gating）

但是，如果只是观察每个独立的观测值，并考虑其分配到每个单独的轨迹上的可能性，这在计算上是愚蠢的。因此我们可以选择忽略每个轨迹定义区域之外的观测值，这称为门控（`gating`），是一种筛选机制。用于确定哪些检测是要进行分配的有效候选目标，哪些应该被完全忽略。

![image-20210324164111765](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324164111.png)

例如使用`JPDA`时，与跟踪目标相距较远的观测值在统计学上对整体解的贡献很小，那么为什么要花费计算资源来计算这个微小的数量呢？特别是如果你要跟踪数十个或数百个对象，这可能会非常浪费资源。所以通过忽略此门外部特定区域之外的观测值，可以加快分配过程。

![image-20210324164234724](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324164234.png)

下面是在`matlab`上的多目标跟踪算法的仿真结果，在此例子中，有两个目标，因此只需要考虑彼此独立运动，通过跟踪雷达观察它们。黑色三角形是目标的真实位置，圆形是雷达站探测到的位置，注意，当两个物体彼此靠近时检测值会发生重叠，很难分辨出目标在这个**模糊区域（Ambiguity region）**中的位置。

![img](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324164312.png)  

所以必须要处理这个数据，让我们试试这些算法，看看它们是如何工作的。

对于第一个算法，由于这些目标是机动的，因此将`GNN`用于数据关联，用`IMM`作为估计滤波器。当目标彼此远离时，哪个目标对应于哪个观测值显而易见，并且`GNN`算法的效果很好，它会将目标1分配给轨迹1，将目标2分配给轨迹2，这就是`GNN`的优势，可以在跟踪目标稀疏时将其与数据进行匹配，但是当目标彼此靠近时，它的效果不理想，可以看到它删除了一条轨迹，并在随后的几次检测中添加了一条新的轨迹（图中轨迹颜色改变了），因此该算法对某一点有多少个目标感到困惑。实际上它从轨迹2跳到了轨迹8，这意味着在确定轨迹6为轨迹8之前，它还维护了其他5条暂留轨迹。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324164430.png"  />

将分配算法升级为`JPDA`算法，很神奇的是，尽管两个目标在实际运动中发生了交叉，两个轨迹仍然在整个机动过程中都保留着，但在模糊区域，误差仍然比其他地方都大，这是意料之中的因为这一区域的数据重叠太多。令人惊讶的是，这些算法可以从这种情况下提取任何东西。

![img](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324164606.png)

现在，与`GNN`相比，`JPDA`的复杂度会带来额外的成本，因此值得评估你的需求是什么，而不仅仅是实现最精确和最复杂的算法，如果目标总是彼此远离，就没必要用`JPDA`，更适合用简单的`GNN`，因为在这种情况下，它能够很好地运行，并且更容易解释和实现。这就是多目标跟踪时需要考虑的事项类型和需要解决的问题的总体要旨。

需要强调的是，没有一种方法可以放之四海而皆准之，这完全取决于每种独特的情况。

视频地址： https://www.youtube.com/watch?v=IIt1LHIHYc4

当传感器检测与跟踪的关联不明确时如何跟踪对象。使用单假设跟踪器（比如GNN），多假设跟踪器（MHT）和概率数据关联跟踪器（JPDA）来比较跟踪器如何处理：

https://ww2.mathworks.cn/help/fusion/ug/tracking-closely-spaced-targets-under-ambiguity.html

![img](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325215542.png) 

`JPDA + IMM`在上面的例子中是最佳的选择。



轨迹融合（track-to-track fusion）/轨迹级融合（track-level fusion）

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210324173323.png" alt="image-20210324173323628" style="zoom:80%;" />

有两种不同的跟踪框架：

**`Central-level tracking（中心级跟踪器）：`**

在这个框架中，传感器的检测结果被输入到一个跟踪算法中，跟踪算法将检测结果分配给轨迹，并更新被跟踪目标的状态和协方差。这里的关键是所有的传感器数据在同一水平，在同一跟踪器中被融合/混合在一起，就像是母舰中有一个集中的单元用以接收所有有用的信息，并进行必要的计算来估计轨迹。有了这个框架，我们可以只用一个传感器，也可以多个传感器混合使用。我们可以跟踪一个目标或者多个目标，目标可以是点目标也可以是`extended object`。只要传感器的测量结果反馈到一个中央跟踪器中，不管它跟踪的是什么，我们都可以将她看作是一个中央级的跟踪器。

![image-20210325161000744](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325161000.png)

**Sensor-level tracking and track-level fusion（传感器级的跟踪器和轨迹级的融合）：**

现在将这种框架与使用传感器级跟踪（`sensor-level tracking`）和轨迹级融合（`track-level fusion`）的架构进行比较。和其他架构一样，一个或多个传感器向中央级跟踪器提供结果。但现在我们有几个这样的跟踪器，每个跟踪器都将自己的一组传感器融合在一起，这些就是这个架构中的传感器级跟踪器，每一个都会产生自己的轨迹估计。现在，我们将所有这些估计轨迹组合/融合到一起，称为一个单一的轨迹集，我们将其称为“使用轨迹级融合器的中心轨迹”。

举个简单的例子， 一个传感器级的跟踪器可能会说，这里有一个目标的概率分布是这样的。另一个传感器级的跟踪器可能会说，这里有一个目标，其概率分布不同。轨迹级融合器需要确定这两条轨迹是两个不同的目标，还是将它们关联为同一个目标。如果是同一个对象，就将两个估计结合起来，创建一个新的状态和概率分布，这个概率分布比任何一个源轨迹单独的概率分布都要准确。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325154225.png" alt="image-20210325154225137" style="zoom:67%;" />

我们可以将这种类型的框架与多个传感器结合使用，并且可以跟踪单个或者多个目标。无论是点目标还是扩展目标，它和中央级跟踪的功能类似，但是方法略有不同，它是用分布式的方法来解决问题。

**现在的问题是，为什么不直接使用单个跟踪器？为什么要通过额外的步骤，拥有多个跟踪器，然后将它们的轨迹融合在一起？**

下面介绍轨迹融合的好处，以及为什么在一些应用场景中，它是更有吸引力的方案。然后再来看看一些挑战。要能判断什么时候该选择第一种架构，什么时候该选择第二种架构。

如果**数据访问、带宽、计算能力和专门化**是你所关心的，那么轨迹级融合（`track level fuser`）对你就是有帮助的。

**（1）数据访问（Access to Data）**：

如果你**无法访问原始传感器数据**，只能得到轨迹信息，就不得不使用轨迹级融合器了。如果你购买的传感器内置了融合和跟踪算法，你也需要使用轨迹级融合器。例如，你可能有一个激光雷达系统，它不返回点云，而是能够跟踪场景中的一些目标，并返回每个目标的轨迹，这里的轨迹可能是一个状态向量，包括位置、速度、方向和形状，以及一组协方差矩阵（`covariance matrices`），显示每个状态的置信度有多高（how much confidence there is in  each state）。在这种情况下，为了将这些轨迹信息与其他传感器相融合，比如说与你的自主车辆上的可见摄像头系统相融合，你就需要一个轨迹级融合器。

![image-20210325161211853](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325161211.png)

**（2）带宽（Bandwidth）**

即使你购买或者构建了传感器可以访问检测结果，你也可能无法将所有信息从传感器**实时地**传输到运行跟踪器的计算单元。有些传感器可以产生的数据速率远远大于通信总线的带宽，比如激光雷达是隐形摄像头，每秒采样几十次，如果你的通信系统内带宽有限，也就是每秒能发送的比特数有限，那么你可能会想要减少每个传感器发送的数据大小。**比如，与相机图像相比，轨迹信息是很小的，因此如果本地计算机能够处理传感器信息，并能将其提炼为对跟踪目标的最佳估计，那么需要发送到运行轨迹级融合器的主计算机上的信息就会少很多。**

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325162404.png" alt="image-20210325162404100" style="zoom: 67%;" />

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325162609.png" alt="image-20210325162609019" style="zoom:67%;" />

**（3）计算能力（Compute）**

即使带宽不是问题，你可以发送所有你想要发送的数据，但仍然可能存在计算能力的问题。设想一下，一辆车上有几十个可见摄像头和激光雷达传感器。一个中央级的跟踪器需要能够在一个巨大的跟踪算法中获取和处理所有的数据，这可能需要耗费很长的处理时间才能以所需的采样率产生估计。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325163745.png" alt="image-20210325163745379" style="zoom: 50%;" />

假设一台本地计算机在处理自己的传感器数据，所有的初始处理都是以并行的方式进行处理，分布在多台计算机中，而轨迹融合算法只需要处理小得多的轨迹信息，从而大大加快了整个处理时间。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325163920.png" alt="image-20210325163920129" style="zoom: 50%;" />

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325210552.png" alt="image-20210325164120927" style="zoom: 80%;" />

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325164344.png" alt="image-20210325164344435" style="zoom: 80%;" />

**（4）Specialization**

也许这些对你来说都不重要，因为假设你有一台强大的计算机，能够一次性处理所有数据。在这种情况下，拥有一个轨迹级的融合器仍然有好处，因为它可以让传感器级的跟踪器专门处理特定的传感器类型。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325165445.png" alt="image-20210325165445795" style="zoom:80%;" />

在跟踪器中，我们必须设置运动模型和传感器模型，并将检测与目标和现有的轨迹相关联。我们还得根据特定的硬件和预期的环境条件等进行调整，而如果我们建立一个专注于融合的跟踪器，比如只融合摄像头数据，那么所有都会变得简单，例如我们可以将这些轨迹与基于激光雷达的跟踪器所产生的轨迹进行融合。这样一来，我们就不会有一个单一的大规模跟踪算法，而是有许多较小的算法，更容易设置、调优和测试。

以上就是使用轨迹级融合算法的好处。那么问题来了，既然轨迹级融合这么好，为什么我们不只使用这种融合方式呢？因为轨迹级融合方式也有一些局限性。

**下面介绍轨迹级融合方式面临的一些挑战。**

**（1）精度降低（Reduced accuracy）:**

传感器会产生很多数据，而跟踪器将这些数据提炼成一个信息量较少的状态向量。作为这个过程的副产品，我们可能会删除一些有用的信息，而删除之后，轨迹级融合器无法再次获取。这样一来，当我们将轨迹融合在一起时，产生的结果会比我们将传感器级的所有信息融合在一起的结果更不准确，也就是说轨迹级融合器比中央级融合器的精度低。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325170519.png" alt="image-20210325170519091" style="zoom:67%;" />

举个例子，我们用两个不同的传感器跟踪同样的两个目标，传感器A有以下检测结果，它的跟踪器生成了左边目标的轨迹，但没有生成右边目标的轨迹，右边的检测会被视为虚假噪声，跟踪器会忽略右边的这些检测，或者也可能是还没有为它建立轨迹。传感器B的情况正好相反，它为右边的目标建立了轨迹，而忽略了左边的检测。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325171040.png" alt="image-20210325171039958" style="zoom:80%;" />

现在将这两条轨迹融合，左边和右边的轨迹都被包含在中央轨迹的列表中，没有被修改，因为没有其他信息用来更新它们。然而，如果我们将所有传感器检测组合，单个检测与其他检测组合，就能帮助改进估计。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325171256.png" alt="image-20210325171255999" style="zoom:80%;" />

轨迹级融合还有一个比较重要的问题，也就是相关的噪声。

**（2）相关噪声（correlated noise）：**

如果我们要融合的轨迹在某种程度上是相关的，那么我们就不能像在标准卡尔曼滤波器中那样，将它们的概率乘在一起。举个简单的例子，想像一下，两个跟踪器使用**同一个过程模型**来预测未来的状态，每个模型初始化时都充分了解目标的状态，这些状态是模型从其各自的完美传感器获得的。当模型将这一完美状态向前传播时，由于过程噪声或模型中的误差，不确定性会增加。我们现在有两个不确定的轨迹估计，我们尝试将这两条轨迹融合在一起，这样我们就有了一个比较可靠的中心估计。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325172102.png" alt="image-20210325172102183" style="zoom:80%;" />

**如果两个不同的模型预测相同的状态，与任何一个单独的解决方案相比，那么我们应该对融合后的解决方案更有信心。**然而，这些轨迹概率是高度相关的，因为它们是用同一个模型生成的，所以事实上，跟单一解决方案相比，我们对融合解决方案的信息没有那么大。因为我们实际上只是运行了两次相同的模型。那么为什么整合结果会给我们更多的信息呢？

如果轨迹之间没有相关性，得益于这一点，我们希望我们的跟踪器增加我们对解决方案的信心。然如果有很大相关性（highly correlated），那么我们希望跟踪器以一种不会增加我们信心的方式来融合解决方案。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325173330.png" alt="image-20210325173330627" style="zoom:67%;" />

但真正的问题在于：我们无从知晓两个轨迹是如何相关的，或者说它们是否相关。处理这种未知的相关性，是现有一些融合算法背后的理念，比如协方差交叉（covariance intersection）。

下面讲讲它的原理。假设一个跟踪器产生了一个概率分布，这个概率分布是一个目标在这个椭圆形的二维平面上的位置；第二个跟踪器产生同一个目标的分布。要将这两个概率融合在一起，我们可以创建第三个概率，以这两个概率的交点为边界。也就是说我们要看这两个椭圆的交点，并完全包含整个交点的分布。可以看到这个分布比之前的任何一个分布都要小，说明我们对解决方案更有信心。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325173812.png" alt="image-20210325173812724" style="zoom: 67%;" />                           <img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325173844.png" alt="image-20210325173843875" style="zoom: 67%;" />          

然而，随着过程噪声或传感器噪声变得更加相关，这两个概率开始对齐，可以看到两个椭圆相交部分是如何增大的，直到两个概率完全对齐，成为完全相同的分布。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325174253.png" alt="image-20210325174253569" style="zoom:67%;" />                        <img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325174321.png" alt="image-20210325174321248" style="zoom:67%;" />

这是一种融合概率的保守方法，可以想像一些分布完全是偶然排列的，完全没有相关性。当这种情况发生时，这个方法仍然会将其当作是相关的。



这个架构中，进入整合器的源轨迹来自传感器级跟踪器。

![image-20210325181002010](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325181002.png)

然而，在某些情况下，源轨迹可能来自其他轨迹级融合器，这就会产生一些一些有趣的现象。

![image-20210325181012260](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325181012.png)

有两个自动驾驶汽车，每个汽车都有自己的一组传感器级跟踪器，这些传感器级跟踪器馈入轨迹级融合器。由于位置关系，后方的车辆看不到前面的行人，但前坊的车辆可以看到，能看到前面行人对后面的车辆很有好处。这样，当行人出现在视野中时，它就无需浪费宝贵的时间建立新轨迹，它已经存在了。为了达到这个目的，两辆车可以共享自己的中心轨迹，并与自己的估计轨迹进行融合。

![image-20210325181100085](https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325181100.png)

现在我们引入一个可能的问题叫做“谣言（rumors）”，它是这样发生的。前车通过后车共享自己的轨迹，告诉后车关于行人的信息，现在两辆车都知道了这个目标，并且用自己的过程模型传播它的状态。每前进一步，前车都会感知到这个目标，并更新它的轨迹，对后车说“嘿，这个目标还在这里”，后车会回复说“是的，我也一直在用我自己的过程模型跟踪它，我们没问题”。现在想像一下，目标消失了，或者离开了传感器的感知范围，前面的车辆可能会放弃跟踪，然后说“嘿，那个目标不见了”，但是正在传播状态的后方车辆可能没有放弃跟踪，它告诉前方车辆“嘿，别担心，我仍然还在跟踪它，这是它的状态信息“，尽管它所做的一切都是在传播前车给它的状态。好了，现在前车会说，”既然你告诉我它还在，我就一直跟踪下去“，此时，一个谣言就产生了，即使没有车辆真正感受到它，但是这个轨迹依然存在。所以轨迹融合算法在设置时，需要阻止谣言的传播，同时不妨碍实际的非谣言轨迹，这非常棘手，关于中央级和轨迹级融合的好处和挑战还有很多，这些是其中主要的。

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325181115.png" alt="image-20210325181115762" style="zoom: 67%;" />

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325181134.png" alt="image-20210325181134387" style="zoom: 67%;" />

<img src="https://raw.githubusercontent.com/zhuifengzhengren10840985/myImage/master/img/20210325181403.png" alt="image-20210325181402873" style="zoom: 67%;" />

