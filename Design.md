OpenCDN Design
--------------

### OpenCDN Job和Task

一个Job可以是一个Task，也可以是多个Task。

1. 增加一个域名
   1. 分发配置文件到CDN节点(ocdn_config)
   2. 节点reload
   3. 反向代理检测
   4. 修改DNS记录(ocdn_dns)
2. 删除一个域名
   1. 修改DNS记录(ocdn_dns)
   2. 删除配置文件(ocdn_config)
   3. 节点Roload
   4. 擦除Cache(ocdn_purge)
3. 擦除Cache(ocdn_purge)
4. 节点流量采集(ocdn_flow)
5. 节点健康状态检测(ocdn_heartbeat)
6. 

### 守护模块
* ocdn_timer 建立一个timer的表，把需要执行的模块和参数放入其中，然后让timer模块来轮询并且触发。
* ocdn_purge 用于刷新缓存<->节点purge
* dns_mode 用于DNS记录变化<->dns服务器或者dnspod等dns服务
* ocdn_config 用户配置文件变更<->节点配置文件
* ocdn_cfg_check(定时) 用户配置文件版本检查<->节点配置文件版本信息(如果有问题则调用ocdn_config进行同步或者调用ocdn_node进行节点排查)注：如果有问题不反复重试，等待定时器的下次检查。
* ocdn_node(定时) 用于检测节点<->节点
* ocdn_flow 流量收集模块(不直接连外网，通过ocdn_node拉取传递过来)

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

1.  如果上面的任意一个Task失败了，怎么确保之前已经成功的Task不重做，并且又能让这次Task重新调度，以及还要保证这个Task不是一个死循环(每次都是失败就有问题了)
2.  最后一个Task做完之后怎么通知JobMaster，并且相应的处理。

### 更多问题可以提出来，可以在上面直接修改，注意增加注释
