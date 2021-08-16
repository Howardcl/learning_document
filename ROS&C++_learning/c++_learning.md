<font color=red size=6>**`gcc、make、makefile、cmake、cmakelists区别`**</font>

1.gcc是GNU Compiler Collection（就是GNU编译器套件），也可以简单认为是编译器，它可以编译很多种编程语言（括C、C++、Objective-C、Fortran、Java等等）。

2.当你的程序只有一个源文件时，直接就可以用gcc命令编译它。

3.但是当你的程序包含很多个源文件时，用gcc命令逐个去编译时，你就很容易混乱而且工作量大

4.所以出现了make工具
make工具可以看成是一个智能的批处理工具，它本身并没有编译和链接的功能，而是用类似于批处理的方式—通过调用makefile文件中用户指定的命令来进行编译和链接的。

5.makefile是什么？简单的说就像一首歌的乐谱，make工具就像指挥家，指挥家根据乐谱指挥整个乐团怎么样演奏，make工具就根据makefile中的命令进行编译和链接的。

6.makefile命令中就包含了调用gcc（也可以是别的编译器）去编译某个源文件的命令。

7.makefile在一些简单的工程完全可以人工手写，但是当工程非常大的时候，手写makefile也是非常麻烦的，如果换了个平台makefile又要重新修改。

8.这时候就出现了Cmake这个工具，cmake就可以更加简单的生成makefile文件给上面那个make用。当然cmake还有其他功能，就是可以跨平台生成对应平台能用的makefile，你不用再自己去修改了。

9.可是cmake根据什么生成makefile呢？它又要根据一个叫CMakeLists.txt文件（学名：组态档）去生成makefile。

10.到最后CMakeLists.txt文件谁写啊？亲，是你自己手写的。

11.当然如果你用IDE，类似VS这些一般它都能帮你弄好了，你只需要按一下那个三角形

# 1.变量、输入输出、表达式和顺序语句

1Byte=8Bit

带宽8Mb=1MB下载速度

| 类型        |                           内容 | 字节数byte |
| ----------- | -----------------------------: | :--------: |
| bool        |                     false/true |     1      |
| char        |                'c','a','','\n' |     1      |
| int         |         -2147483648~2147483647 |     4      |
| float       | 1.23,2,5,1,235e2,6-7位有效数字 |     4      |
| double      |                15-16位有效数字 |     8      |
| long long   |                   -2^63~2^63-1 |     8      |
| long double |                18-19位有效数字 |  16 12 8   |

ACwing 题库状态

```c++
Accepted  

time limit error 超时

memory limit error 超内存
    
Segmentation Fault 数组溢出
    
Float Point Exception 浮点数异常
```

所有能用cout cin 的地方，都能用scanf printf

但是用scanf printf的地方，不一定能用cout cin ，因为scanf 和printf的效率更高。

```c++
scanf("%c%c",a,b);//%c是会读入空格的,故输入时要注意是否有空格输入。
cin >> a >> b;// cin会自动过滤空格
scanf("%lf%lf",a,b);//double类型的读入用lf控制
scanf("%lld%lld",a,b);//long long类型的读入用lld控制
/*
int : %d
float : %f
char : %c
double : %lf
long long : %lld
*/
```

对于整数相除的话是整除。对两个浮点数而言，相除得到小数。

![image-20210627110505585](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210627110505585.png)

整型变量的自增、自减：

![image-20210627111024902](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210627111024902.png)

前自增和后自增对于变量a本身来说是没有任何区别的，但是对于```int b = a ++ ;```而言，是先将a赋给b，然后a再自增。

**隐式类型转换：如果两个不同类型的变量做运算，会默认把精度比较低的类型转换为精度比较高的类型。**

# 2.循环结构

cin 本身是有返回值的，如果cin读到0的话表示没有读到值，而是读到了文件结束符。（EOF 或-1）

```c++
#include<iostream>
using namespace std;

int main()
{
    int x;
    while(cin >> x && x) //表示当x是0的话，再判断是否进入；关系到cin读入0的问题
    {
        for(int i = 1;i <= x;i++)
        {
            cout << i << " ";
        }
        cout << endl;
    }
    return 0;
}
```

![image-20210712191449040](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210712191449040.png)

![image-20210712190545511](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210712190545511.png)

<font color=red size=6>解法：C++代码</font>

```c++
#include<iostream>
#include<cmath>
using namespace std;
/*
两点之间的曼哈顿距离：(x1,y1) (x2,y2)
|x2-x1|+|y2-y1|为曼哈顿距离
首先求中心点坐标,再判断各个点离中心点的距离，以此决定是否输出'*'
*/
int main()
{
    int n;
    cin >> n;
    
    //找中心点
    int center_x = n/2,center_y=n/2;
    
    for(int i = 0;i < n;i++)
    {
        for(int j = 0;j < n;j++)
        {
            if(abs(i-center_x)+abs(j-center_y) <= n/2)   cout << "*" ;
            else cout << " ";
        }
        cout << endl;
    }
    return 0;
}
```

# 3.数组

![image-20210712211043757](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210712211043757.png)

``` c++
#include<iostream>
using namespace std;

double C(int a,int b)//求组合数
{
    double res = 1;
    for(int i = 1,j = a;i <= b;i++,j--)
    {
        res = res*j/i;
    }
    return res;
}
int main()
{
    cout << C(10,2) << endl;
    return 0;
}
```

``` c++
//浮点数的有效位数：double是16位有效数字
int a = 3;
if(sqrt(a) * sqrt(a) < 3)  puts("!!!");
```

```c++
#include<algorithm>：
algorithm意为"算法",是C++的标准模版库（STL）中最重要的头文件之一，提供了大量基于迭代器的非成员模版函数。

accumlate ： iterator 对标志的序列中的元素之和，加到一个由 init 指定的初始值上。重载的版本不再做加法，而是传进来的二元操作符被应用到元素上。

adjacent_different ：创建一个新序列，该序列的每个新值都代表了当前元素与上一个元素的差。重载版本用指定的二元操作计算相邻元素的差。

adjacent_find ：在 iterator 对标志的元素范围内，查找一对相邻的重复元素，如果找到返回一个 ForwardIterator ，指向这对元素的第一个元素。否则返回 last 。重载版本使用输入的二元操作符代替相等的判断。

binary_search ：在有序序列中查找 value ，如果找到返回 true 。重载的版本使用指定的比较函数对象或者函数指针来判断相等。

copy ：复制序列。

copy_backward ：除了元素以相反的顺序被拷贝外，别的和 copy 相同。

count ：利用等于操作符，把标志范围类的元素与输入的值进行比较，并返回相等元素的个数。

count_if ：对于标志范围类的元素，应用输入的操作符，并返回结果为 true 的次数。

equal ：如果两个序列在范围内的元素都相等，则 equal 返回 true 。重载版本使用输入的操作符代替了默认的等于操作符。

equal_range ：返回一对 iterator ，第一个 iterator 表示由 lower_bound 返回的 iterator ，第二个表示由 upper_bound 返回的 iterator 值。

fill ：将输入的值的拷贝赋给范围内的每个元素。

fill_n ：将输入的值赋值给 first 到 frist+n 范围内的元素。

find ：利用底层元素的等于操作符，对范围内的元素与输入的值进行比较。当匹配时，结束搜索，返回该元素的一个 InputIterator 。

find_if ：使用输入的函数替代了等于操作符执行了 find 。

find_end ：在范围内查找“由输入的另外一个 iterator 对标志的第二个序列”的最后一次出现。重载版本中使用了用户输入的操作符替代等于操作。

find_first_of ：在范围内查找“由输入的另外一个 iterator 对标志的第二个序列”中的任意一个元素的第一次出现。重载版本中使用了用户自定义的操作符。

for_each ：依次对范围内的所有元素执行输入的函数。

generate ：通过对输入的函数 gen 的连续调用来填充指定的范围。

generate_n ：填充 n 个元素。

includes ：判断 [first1, last1) 的一个元素是否被包含在另外一个序列中。使用底层元素的 <= 操作符，重载版本使用用户输入的函数。

inner_product ：对两个序列做内积 ( 对应的元素相乘，再求和 ) ，并将内积加到一个输入的的初始值上。重载版本使用了用户定义的操作。

inner_merge ：合并两个排过序的连续序列，结果序列覆盖了两端范围，重载版本使用输入的操作进行排序。

iter_swap ：交换两个 ForwardIterator 的值。

lexicographical_compare ：比较两个序列。重载版本使用了用户自定义的比较操作。

lower_bound ：返回一个 iterator ，它指向在范围内的有序序列中可以插入指定值而不破坏容器顺序的第一个位置。重载函数使用了自定义的比较操作。

max ：返回两个元素中的较大的一个，重载版本使用了自定义的比较操作。

max_element ：返回一个 iterator ，指出序列中最大的元素。重载版本使用自定义的比较操作。

min ：两个元素中的较小者。重载版本使用自定义的比较操作。

min_element ：类似与 max_element ，不过返回最小的元素。

merge ：合并两个有序序列，并存放到另外一个序列中。重载版本使用自定义的比较。

mismatch ：并行的比较两个序列，指出第一个不匹配的位置，它返回一对 iterator ，标志第一个不匹配的元素位置。如果都匹配，返回每个容器的 last 。重载版本使用自定义的比较操作。

next_permutation ：取出当前范围内的排列，并将其重新排序为下一个排列。重载版本使用自定义的比较操作。

nth_element ：将范围内的序列重新排序，使所有小于第 n 个元素的元素都出现在它前面，而大于它的都出现在后面，重载版本使用了自定义的比较操作。

partial_sort ：对整个序列做部分排序，被排序元素的个数正好可以被放到范围内。重载版本使用自定义的比较操作。

partial_sort_copy ：与 partial_sort 相同，除了将经过排序的序列复制到另外一个容器。

partial_sum ：创建一个新的元素序列，其中每个元素的值代表了范围内该位置之前所有元素之和。重载版本使用了自定义操作替代加法。

partition ：对范围内元素重新排序，使用输入的函数，把计算结果为 true 的元素都放在结果为 false 的元素之前。

prev_permutation ：取出范围内的序列并将它重新排序为上一个序列。如果不存在上一个序列则返回 false 。重载版本使用自定义的比较操作。

random_shuffle ：对范围内的元素随机调整次序。重载版本输入一个随机数产生操作。

remove ：删除在范围内的所有等于指定的元素，注意，该函数并不真正删除元素。内置数组不适合使用 remove 和remove_if 函数。

remove_copy ：将所有不匹配的元素都复制到一个指定容器，返回的 OutputIterator 指向被拷贝的末元素的下一个位置。

remove_if ：删除所有范围内输入操作结果为 true 的元素。

remove_copy_if ：将所有不匹配的元素拷贝到一个指定容器。

replace ：将范围内的所有等于 old_value 的元素都用 new_value 替代。

replace_copy ：与 replace 类似，不过将结果写入另外一个容器。

replace_if ：将范围内的所有操作结果为 true 的元素用新值替代。

replace_copy_if ：类似与 replace_if ，不过将结果写入另外一个容器。

reverse ：将范围内元素重新按反序排列。

reverse_copy ：类似与 reverse ，不过将结果写入另外一个容器。

rotate ：将范围内的元素移到容器末尾，由 middle 指向的元素成为容器第一个元素。

rotate_copy ：类似与 rotate ，不过将结果写入另外一个容器。

search ：给出了两个范围，返回一个 iterator ，指向在范围内第一次出现子序列的位置。重载版本使用自定义的比较操作。

search_n ：在范围内查找 value 出现 n 次的子序列。重载版本使用自定义的比较操作。

set_difference ：构造一个排过序的序列，其中的元素出现在第一个序列中，但是不包含在第二个序列中。重载版本使用自定义的比较操作。

set_intersection ：构造一个排过序的序列，其中的元素在两个序列中都存在。重载版本使用自定义的比较操作。

set_symmetric_difference ：构造一个排过序的序列，其中的元素在第一个序列中出现，但是不出现在第二个序列中。重载版本使用自定义的比较操作。

set_union ：构造一个排过序的序列，它包含两个序列中的所有的不重复元素。重载版本使用自定义的比较操作。

sort ：以升序重新排列范围内的元素，重载版本使用了自定义的比较操作。

stable_partition ：与 partition 类似，不过它不保证保留容器中的相对顺序。

stable_sort ：类似与 sort ，不过保留相等元素之间的顺序关系。

swap ：交换存储在两个对象中的值。

swap_range ：将在范围内的元素与另外一个序列的元素值进行交换。

transform ：将输入的操作作用在范围内的每个元素上，并产生一个新的序列。重载版本将操作作用在一对元素上，另外一个元素来自输入的另外一个序列。结果输出到指定的容器。

unique ：清除序列中重复的元素，和 remove 类似，它也不能真正的删除元素。重载版本使用了自定义的操作。

unique_copy ：类似与 unique ，不过它把结果输出到另外一个容器。

upper_bound ：返回一个 iterator ，它指向在范围内的有序序列中插入 value 而不破坏容器顺序的最后一个位置，该位置标志了一个大于 value 的值。重载版本使用了输入的比较操作。

堆算法： C++ 标准库提供的是 max-heap 。一共由以下 4 个泛型堆算法。

make_heap ：把范围内的元素生成一个堆。重载版本使用自定义的比较操作。

pop_heap ：并不是真正的把最大元素从堆中弹出，而是重新排序堆。它把 first 和 last-1 交换，然后重新做成一个堆。可以使用容器的 back 来访问被“弹出“的元素或者使用 pop_back 来真正的删除。重载版本使用自定义的比较操作。

push_heap ：假设 first 到 last-1 是一个有效的堆，要被加入堆的元素在位置 last-1 ，重新生成堆。在指向该函数前，必须先把元素插入容器后。重载版本使用指定的比较。

sort_heap ：对范围内的序列重新排序，它假设该序列是个有序的堆。重载版本使用自定义的比较操作。
```

<font size =6>**蛇形矩阵-题目描述**</font>

输入两个整数n和m，输出一个n行m列的矩阵，将数字 1 到 n*m 按照回字蛇形填充至矩阵中。

具体矩阵形式可参考样例。

**输入格式**
输入共一行，包含两个整数n和m。

输出格式
输出满足要求的矩阵。

矩阵占n行，每行包含m个空格隔开的整数。

**数据范围**
1≤n,m≤100

**样例**
输入样例：
3 3

输出样例：
1 2 3
8 9 4
7 6 5

``` c++
#include <iostream>

using namespace std;

int m,n;

int const N = 110;

int f[N][N];

int main()
{
    cin >> n >> m;
    int dx[4] = { 0, 1, 0, -1};
    int dy[4] = { 1, 0, -1, 0};//准备两个数值表示当前行走方向 依此为 东-南-西-北-东-...(右-下-左-上-右-...) 
    int x = 1, y = 1,d = 0;//x,y表示从(1,1)点开始行走 ， d表示初始方向为东  
    for(int i = 1; i <= n * m; i ++)
    {
        if((x + dx[d] > n || y + dy[d] > m || y + dy[d] == 0) || (f[x + dx[d]][y + dy[d]]))//判断行走的下一个状态是否碰壁 
        //( 下移时是否碰越下界 || 右移时是否越右界  || 左移时是否越左界) || (若不改变移动方向 下一点是否已经到达过)
        d = (d + 1) % 4;//碰壁后换移动方向 
        f[x][y] = i;//标记当前到达点 
        x += dx[d];
        y += dy[d];//以当前方向(可能改变也可能未改变)移动一次 
    }
    for(int i = 1; i <= n; i ++)
    {
        for(int j = 1;j <= m; j ++)
            cout << f[i][j] << ' ';
        cout << endl;
    }//输出 
    return 0;
}


```

# 4.字符串

<font size=5>**求字符串长度-题目描述**</font>
给定一行长度不超过100的字符串，请你求出它的具体长度。

<font size=5>输入格式</font>
输入一行，表示一个字符串。注意字符串中可能包含空格。

<font size=5>**输出格式**</font>
输出一个整数，表示它的长度。

<font size=5>**样例**</font>

输入样例：

``` I love Beijing.```
输出样例：
```15```

**算法1**
C语言代码

```c++
#include<string.h>
#include<stdio.h>

int main()
{
    char s[105];
    gets(s);
    printf("%d",strlen(s));
    return 0;
}
```

**算法2**
C++ 代码（常用）

```c++
#include <iostream>
#include <cstring>

using namespace std;

int main()
{
    string a;
    getline(cin,a);
    cout<<a.size()<<endl;
    return 0;
}
```

**算法3**
C++ 代码

```c++
#include <iostream>
#include <cstring>

using namespace std;

int main()
{
    char a[105];
    cin.get(a,105);//需要注意cin.get()不会把换行符取出删除，会读入换行符，会使字符数组长度增加1，影响下一次读入！
    cout<<strlen(a)<<endl;
    return 0;
}
```

<font size=5>==cin 和 scanf读入字符串时遇到空格就停止了。==</font>

<font size=5>==但getline可以完美处理一行字符（不管是否有空格）的输入==</font>

```c++
string s;
getline(cin,s);
cout << s << endl;
```

<font size=8>[gets(), getline(), cin.getline()](https://www.cnblogs.com/hi3254014978/p/12247076.html)</font>

gets(str), getline(cin, s), cin.getline(str, len),这三个函数都是读入一行字符串的函数，下面是这三个函数的区别

**1. gets()** 函数是 C 语言的函数，它接受的参数是字符数组， gets输入字符串时，不进行数组下标的检查，也就是说当你的数组长度是n时，输入超过该长度的字符串的时候，编译不会出错，但是运行的时候会出现数组越界或者内存泄漏的错误，所以现在有部分编译器已经不支持这个函数了，比如 PTA 就已经不支持这个函数了。***gets()\*函数**的用法如下：

```c++
char str[20];
gets(str);
```

 

2. ***getline()*** 函数是 C++ 函数，他接受的参数是 一个输入流和一个string类型的字符串，要使用这个函数必须加上 ***#include <string>\*** 这个头文件和 ***using name space std;\*** 这个命名空间。getline()函数的用法如下：

```c++
#include <string>
using namespace std;

string s;
getline(cin, s);
```

 

3. ***cin.getline()***函数也是 C++ 函数，它接受的参数是一个 C风格字符串（也就是一个字符数组），和一个最大长度，要使用这个函数，必须加上***#include <iostream>*** 这个头文件 和***using namespace std;***这个命名空间。cin.getline()函数的用法如下：

```c++
#include <iostream>
using namespace std;

char str[20];
cin.getline(str, 20);
```

**注意：**（1）cin.getline()实际上有三个参数，cin.getline(接收字符串的变量,接收字符个数,结束字符)
　　　（2）当第三个参数省略时，系统默认为'\n'

==cin>>遇“空格”、“TAB”、“回车”就结束==

``` c++
用法1：输入一个数字或字符
#include <iostream>
using namespace std;
int main ()
{
    int a,b;
    cin>>a>>b;
    cout<<a+b<<endl;
}
用法2：接收一个字符串，遇“空格”、“TAB”、“回车”就结束
#include <iostream>
using namespace std;
int main ()
{
    char a[20];
    cin>>a;
    cout<<a<<endl;
}

例如：

输入：jkljkljkl
输出：jkljkljkl

输入：jkljkl jkljkl //遇空格结束
输出：jkljkl
```



**不可以用scanf读入string**

```c++
string s;
scanf("%s",&s);
cout << s << endl;
//这样写是会报错的
```

**但可以用printf输出string**

``` c++
printf("%s\n",s.c_str())//将字符串转换为字符数组输出
```

**注意：fgets和gets的区别：**

fgets会把回车符的长度也读入进来，不会过滤掉回车，而gets会过滤掉回车（c++17后已经把gets删掉了）

**基于范围的for语句：**

![image-20210813153137078](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210813153137078.png)

使用取地址符&，在改变c的同时，也改变s。

<font size=6>==**stringstream的作用**==</font>

**<font size=5>单词替换-题目描述：</font>**

输入一个字符串，以回车结束（字符串长度不超过 100100）。

该字符串由若干个单词组成，单词之间用一个空格隔开，所有单词区分大小写。

现需要将其中的某个单词替换成另一个单词，并输出替换之后的字符串。

<font size=5>**输入格式**</font>

输入共 33 行。

第 11 行是包含多个单词的字符串 ss;

第 22 行是待替换的单词 aa(长度不超过 100100);

第 33 行是 aa 将被替换的单词 bb(长度不超过 100100)。

<font size=5>**输出格式**</font>

共一行，输出将 ss 中所有单词 aa 替换成 bb 之后的字符串。

**输入样例**：

```
You want someone to help you
You
I
```

**输出样例：**

```
I want someone to help you
```

``` c++
#include<iostream>
#include<string>
#include<sstream>
using namespace std;

int main()
{
    string s,a,b;
    getline(cin,s);
    cin >> a >> b;
    // 怎么把s当中的a都找出来？
    stringstream ssin(s);//把字符串初始化为字符串流
    /**
    stringstream的用处：可以从字符串中提取出来我们需要的各种信息
    int a,b;
    string str;
    double c;
    ssin >> a >> b >> str >> c;
    cout << a << endl << str << endl << b << endl << c << endl;
    能够提取出来不同类型的字符
    eg：
    输入： 123 yxc 321 1.123
    输出：
    123
    yxc
    321
    1.123
    */
    string str;
    while(ssin >> str)
    {
        if(str == a) cout << b << ' ';
        else cout << str << ' ';
    }
    return 0;
}
```

# 5.函数

<font size=6>==**在工程上，一般不写using namespace std**==</font>

而是写std::，因为工程上有很多的命名空间，不同命名空间中的变量名可能会重复。

**函数的声明与定义，在写大工程时是有用的，将声明与定义分开，在需要看函数具体实现时才去看函数定义**

<font size=6>==**静态变量**==</font>

静态变量的初始化只会在第一次调用的时候初始化，第二次调用的时候不会再初始化

等于在函数内部开了一个只有该函数能用的全局变量

静态变量会开辟在堆空间中

```c++
int output(void)
{
    static int cnt = 0;
    cnt++;
    cout << "call: " << cnt << "times" << endl;
}
int main()
{
    output();
    output();
    output();
    output();
    output();
    return 0;
}
输出：
call: 1times
call: 2times
call: 3times
call: 4times
call: 5times
```

**判断函数是否一样：根据函数名和形参类型**

<font size=6>==**函数--数组形参**==</font>

**一维数组形参的写法：**

``` c++
// 尽管形式不同，但这三个print函数是等价的
void print(int * a) {/* … */}
void print(int a[]) {/* … */}
void print(int a[10]) {/* … */}
```

**多维数组形参的写法：**

``` c++
// 多维数组中，除了第一维之外，其余维度的大小必须指定
void print(int (*a)[10]) {/* … */}
void print(int a[][10]) {/* … */}
```

**函数形参的默认值，只能出现在后面的几个形参，不能前面的形参有默认值，后面的形参没有默认值。**

**==内联函数：在返回值类型前加inline关键字==**

作用：编译器不把函数识别为函数了，在所有调用函数的地方，用函数体替换。

递归：不支持内联函数

**![image-20210815101313111](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210815101313111.png)**

<font size=6>==**递归**==</font>

在一个函数内部，也可以调用函数本身。

![image-20210815104936168](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210815104936168.png)

**<font size=5>数组翻转-题目描述</font>**

给定一个长度为 n的数组 a 和一个整数 size，请你编写一个函数，`void reverse(int a[], int size)`，实现将数组 a 中的前 sizesize 个数翻转。

输出翻转后的数组 a。

<font size=5>**输入格式**</font>

第一行包含两个整数 nn 和 sizesize。

第二行包含 nn 个整数，表示数组 aa。

<font size=5>**输出格式**</font>

共一行，包含 nn 个整数，表示翻转后的数组 aa。

<font size=5>**数据范围**</font>

1≤size≤n≤10001≤size≤n≤1000

**<font size=5>输入样例：</font>**

```
5 3
1 2 3 4 5
```

<font size=5>**输出样例**</font>

```
3 2 1 4 5
```

``` c++
#include<iostream>

using namespace std;
/**翻转思路：双指针，一个指向0，一个指向最后size
 * 然后将两个指针指向的值交换，然后一个指针后移，一个指针前移
 * 直到相等的时候停下来
 */
void reverse(int a[],int size)
{
    for(int i = 0,j = size - 1;i < j;i++,j--)
    {
        swap(a[i],a[j]);
    }
}
int main()
{
    int n,size;
    cin >> n >> size;
    int a[1000];
    for(int i = 0;i < n;i++) cin >> a[i];
    reverse(a,size);
    for(int i = 0;i < n;i++) cout << a[i] << ' ';
    return 0;
}
```

```c++
#include<iostream>

using namespace std;
/**怎样对数组进行从小到大排序？
 * 选择排序：复杂度n*n
 * 第一重循环：修改当前数
 * 第二重循环：让当前数与后面的数比较
 */
void sort(int a[],int l,int r)
{
    for(int i = l;i <= r;i++)
    {
        for(int j = i + 1;j <= r;j++)
            if(a[j] < a[i]) swap(a[i],a[j]);
    }
}

int main()
{
    int n,l,r;
    int a[1000];
    cin >> n >> l >> r;
    for(int i = 0;i < n;i++) cin >> a[i];
    sort(a,l,r);
    for(int i = 0;i < n;i++) cout << a[i] << ' ';
    return 0;
}
```

**<font size=5>跳台阶-题目描述</font>**

一个楼梯共有 n级台阶，每次可以走一级或者两级，问从第 0级台阶走到第 n级台阶一共有多少种方案。

<font size=5>**输入格式**</font>

共一行，包含一个整数 n。

<font size=5>**输出格式**</font>

共一行，包含一个整数，表示方案数。

<font size=5>**数据范围**</font>

1≤n≤15

**<font size=5>输入样例：</font>**

```
5
```

输出样例：

```
8
```

![image-20210816110650402](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210816110650402.png)

``` c++
#include<iostream>

using namespace std;
/**思路：递归--->枚举所有方案：可以通过画递归搜索树的方式来理清思路
 * 
 */
int n;//台阶数，全局变量
int ans = 0;//方案，全局变量
void f(int k)
{
    if(k == n)  ans++;
    else if(k < n) 
    {
        f(k+1);
        f(k+2);
    }
    else return;
}
int main()
{
    cin >> n;
    f(0);//从0开始走
    cout << ans;
    return 0;
}
```



==**<font size=5>排列-题目描述</font>**==

给定一个整数 n，将数字 1∼n排成一排，将会有很多种排列方法。

现在，请你按照字典序将所有的排列方法输出。

<font size=5>**输入格式**</font>

共一行，包含一个整数 n。

<font size=5>**输出格式**</font>

按字典序输出所有排列方案，每个方案占一行。

<font size=5>**数据范围**</font>

1≤n≤9

**<font size=5>输入样例：</font>**

```
3
```

输出样例：

```
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
```



![image-20210816153507532](https://raw.githubusercontent.com/Howardcl/MyImage/main/img/image-20210816153507532.png)



``` c++
#include<iostream>

using namespace std;
/**字典序：比较两个序列的一种方式，从头开始比较，有不同的字符，
 * 比较小的字符所在的字符串就比较小
 * 
 */
 
const int N = 10;
int n;
//int u形参的作用是控制枚举到了哪里
//nums的作用是存储排列的数组
//state的作用是判断数字之前用过没有
void dfs(int u,int nums[],bool state[])
{
    if(u > n)//代表枚举完了，直接输出排列后的数组即可
    {
        for(int i = 1;i <= n;i++) cout << nums[i] << ' ';
        cout << endl;
    }
    else
    {
        for(int i = 1;i <= n;i++)
        {
            if(!state[i]) //代表这个数字没用过
            {
                state[i] = true;
                nums[u] = i;
                dfs(u + 1,nums,state);
                state[i] = false;//一次排列完毕后，恢复现场
            }
        }
    }
}
int main()
{
    cin >> n;
    int nums[N];//存每个位置放的数
    bool state[N] = {0};//判断每个数有没有被用过
    
    dfs(1,nums,state);//从第一个位置开始枚举
    return 0;
}
```

