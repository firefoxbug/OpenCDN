OpenCDN Design
--------------

### OpenCDN Job和Task

一个Job可以是一个Task，也可以是多个Task。

1. 增加一个域名
   1. 分发配置文件到CDN节点
   2. 节点reload
   3. 反向代理检测
   4. 修改DNS记录
2. 删除一个域名
   1. 修改DNS记录
   2. 删除配置文件
   3. 节点Roload
   4. 擦除Cache
3. 擦除Cache(Purge模块)
4. 节点流量采集(Flow模块)
5. 节点健康状态检测(Hearbeat模块)

### 如何执行一个Job

1.  OpenCDN中基本执行单元都是Task，一个Job可以包含一个或多个Task。
2.  每个Job都有一个Json文件来描述所有Task执行流程以及Task之间的数据传输。
3.  每一种Task都有一个队列，队列的消费者是一启动就存在的。

比如执行一个增加域名的Job，那么有几个Task组成一个有向图(DAG)，通过下面来执行。

> 注：所有Task都已经运行，每个Task都有自己一个队列，所做的就是消费队列中的任务。 引入一个JobMaster的概念，JobMaster就是负责发起Job的。

1.  JobMaster要发起一个Job，比如指定一个增加域名的Job json描述文件，总共需要4个Task完成，比如分别是A,B,C,D
    <pre>
    {
      'Description': 'Add a domain',
      'TaskList'   : ['A','B','C','D'],
      'A':{
    'Parameter': 'www.firefoxbug.com'
      },
      'B':{
    'Parameter': ''
      },
      'C':{
    'Parameter': ''
      },
      'D':{
    'Parameter': ''
      }
    }
    </pre>
2.  把上面的Job丢到TaskA所在的队列，TaskA取出，根据参数执行TaskA任务
3.  如果TaskA执行成功则修改json文件为如下
    <pre>
    {
      'Description': 'Add a domain',
      'TaskList'   : ['B','C','D'],
      'B':{
    'Parameter': 'www.firefoxbug.com'
      },
      'C':{
    'Parameter': ''
      },
      'D':{
    'Parameter': ''
      }
    }
    </pre>
4.  TaskA根据TaskList把json文件丢到TaskB所在队列。
5.  依次进行上面的循环直到TaskList为空。

两个问题大家可以讨论下:

1.  如果上面的任意一个Task失败了，怎么确保之前已经成功的Task不重做，并且又能让这次Task重新调度，已经还要保证这个Task不是一个死循环(每次都是失败就有问题了)
2.  最后一个Task做完之后怎么通知JobMaster，并且相应的处理。

### 更多问题可以提出来，可以在上面直接修改，注意增加注释