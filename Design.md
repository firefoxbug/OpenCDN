OpenCDN Design
--------------

### OpenCDN Job和Task

一个Job可以是一个Task，也可以是多个Task。

1. 增加一个域名
   1. 分发配置文件到CDN节点(ocdn_config)
   2. 节点reload(ocdn_config)
   3. 反向代理检测(ocdn_proxy)
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

> 注：所有Task都已经运行，每个Task都有自己一个队列，所做的就是消费队列中的任务。

<pre>
{
  'TaskName' : 'ADD_DOMAIN',  #Task名字
  'Description' : 'add a Domain' # Job所描述
  'TaskList' : ['OCDN_PUSH_CONF','OCDN_RELOAD','OCDN_PROXY','OCDN_DNS'], #Job所有Task列表
  'CurrentTask': 'OCDN_PUSH_CONF', #当前要执行的Task,
  'TimeOut' : 10 #10秒,
  'RunTimesLimit': #Task运行最大次数
  {
    'AlreadyRunTimes': 0, #当前执行该Task次数
    'MaxRunTimes' : 10    #最多执行该Task次数
  },
  'Parameters': #参数
  {
    'Domain':'www.firefoxbug.com',
    'Node':'192.168.1.1'
  }
}
</pre>
三个问题大家可以讨论下:

1.  如果上面的任意一个Task失败了，怎么确保之前已经成功的Task不重做，并且又能让这次Task重新调度，以及还要保证这个Task不是一个死循环(每次都是失败就有问题了)
    
	解决方案：引入了RunTimesLimit这个配置，如果Task执行失败，可以重新调度，AlreadyRunTimes加1，直到超过MaxRunTimes后就判定Task为失败。

2.  任务堆积功能考虑，对于cdn节点，挂掉是常态，而这个会导致任务的不一致性。一种是采用队列进行堆积任务，可能数据会太热。有些节点挂几个月，就会占用很多的热存储资源。另一种是等节点重新起来之后再去找哪些任务没做过，然后拉出来做。这个会导致编程的逻辑过于复杂。我考虑的一种方案是，在本地建一个虚拟节点，所有的配置文件数据全部旁路传一份到虚拟节点。然后一旦一个节点挂掉了的话，从虚拟节点rsync(或者类似的原理)一份到实体节点，然后就迅速追回到最新状态开始工作。


### 更多问题可以提出来，可以在上面直接修改，注意增加注释



