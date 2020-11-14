# MyKMeans

- 实现基于Hadoop的KMeans算法

## 运行说明

 - 输入参数
    - cluster_number：聚类数量
    - iterate_number：迭代次数
   - input_path：输入路径，该路径下可以有多个文件
   - output_path：输出路径（再次执行时要确保该目录尚不存在）
   ```
     hadoop jar target/mykmeans-1.0.jar cluster_number iterate_number input_path output_path
   ```

## 设计思路

- 每个map节点读取上一次迭代生成的cluster centers，判断自己节点上的数据归属于哪个cluster
- reduce节点计算每个cluster的数据点，计算出新的cluster centers
- 项目结构设计
  - Instance.java：以ArrayList存放数据点的各个分量，对应文件中原始数据点的格式。边写加法、乘法、除法函数用于计算簇中心。
  - Cluster.java：记录簇的信息，包括id、数据点个数、簇中心
  - KMeans.java：实现KMeans算法。mapper读取每个数据点，通过计算欧氏距离，选择距离最小的簇中心，并输出分类结果；combiner计算新的簇中心；reducer将计算结果进行汇总，计算全局的簇中心。
  - KMeansCluster.java：在最终产生结果后，再对输入文件中的所有实例进行分簇，最后把实例按照（实例，簇id）的方式写入结果文件
  - KMeansDriver.java：启动MapReduce，读取参数
  - RandomClusterGenerator.java：随机生成簇中心
  - Utils：计算距离

## 运行情况

### 输出结果

<img src="images/image-20201029124031317.png" alt="image-20201029124031317"  />![images/image-20201029124053010](images/image-20201029124053010.png)![images/image-20201029124108730](images/image-20201029124108730.png)

### 监控

#### Yarn

![images/image-20201029124346607](images/image-20201029124346607.png)

#### HDFS 

![images/image-20201029124437596](images/image-20201029124437596.png)

![images/image-20201029124502341](images/image-20201029124502341.png)

![images/image-20201029124537749](images/image-20201029124537749.png)

## 主要问题

### `cleanup()`中输出问题

在思路一进行输出时，将String变量与其他常量进行合并，会出现其他常量重复两次的现象（尝试输出发现是合并操作时改变了String变量的值，但只会在有`context.write()`操作时改变，当不进行此操作时不改变）。

错误输出现象如下：

![images/image-20201029125016521](images/image-20201029125016521.png)

但若使用TreeSet进行排序，在仅用一个Job的情况下只能将`context.write()`写入`cleanup()`，因此之后采用思路二作为最终版本。当不需要改变输入格式时，采用思路一的输出是正常的。