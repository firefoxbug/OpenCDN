
|  TaskName         |  含义       
| ----------------- |:-------------:
| OCDN_ADD_NODE   | 添加节点
| OCDN_DEL_NODE   | 添加节点
| OCDN_ADD_DOMAIN   | 添加域名
| OCDN_DEL_DOMAIN   | 删除域名
| OCDN_REMOVE_CONF  | 删除配置文件 
| OCDN_SYNC_CONF  | 同步配置文件 
| OCDN_VER_CONF  | 查看配置文件的版本
| OCDN_RELOAD_NODE       | 节点reload
| OCDN_PROXY        | 节点proxy检测
| OCDN_ADD_DNS      | 增加DNS
| OCDN_DEL_DNS      | 撤销DNS
| OCDN_PURGE  		| 擦除缓存

### 增加域名
<pre>
{
	'TaskName' : 'OCDN_ADD_DOMAIN',	#Task名字
	'Description' : 'add a Domain' # Job所描述
	'TaskList' : ['OCDN_PUSH_CONF','OCDN_RELOAD_NODE','OCDN_PROXY','OCDN_ADD_DNS'], #Job所有Task列表
	'CurrentTask': 'OCDN_PUSH_CONF', #当前要执行的Task,
	'TimeOut' : 10 #10秒,
	'RunTimesLimit': #Task运行最大次数
	{
		'AlreadyRunTimes': 0,	#当前执行该Task次数
		'MaxRunTimes' : 10 		#最多执行该Task次数
	},
	'Parameters': #参数
	{
		'Domain':'www.firefoxbug.com',
		'Node':['192.168.1.1','192.168.1.2']
	}
}
</pre>

### 删除域名
<pre>
{
	'TaskName' : 'OCDN_DEL_DOMAIN',	#Task名字
	'Description' : 'del a Domain' # Job所描述
	'TaskList' : ['OCDN_DEL_DNS'，'OCDN_DEL_CONF','OCDN_RELOAD'], #Job所有Task列表
	'CurrentTask': 'OCDN_PUSH_CONF', #当前要执行的Task,
	'TimeOut' : 10 #10秒,
	'RunTimesLimit': #Task运行最大次数
	{
		'AlreadyRunTimes': 0,	#当前执行该Task次数
		'MaxRunTimes' : 10 		#最多执行该Task次数
	},
	'Parameters': #参数
	{
		'Domain':'www.firefoxbug.com',
		'Node':['192.168.1.1','192.168.1.2']
	}
}
</pre>

### 增加节点
<pre>
{
	'TaskName' : 'OCDN_ADD_NODE',	#Task名字
	'Description' : 'del a Node' # Job所描述
	'TaskList' : ['OCDN_ADD_NODE'，'OCDN_SYNC_CONF','OCDN_RELOAD_NODE'], #Job所有Task列表
	'CurrentTask': 'OCDN_ADD_NODE', #当前要执行的Task,
	'TimeOut' : 10 #10秒,
	'RunTimesLimit': #Task运行最大次数
	{
		'AlreadyRunTimes': 0,	#当前执行该Task次数
		'MaxRunTimes' : 10 		#最多执行该Task次数
	},
	'Parameters': #参数
	{
		'Node':'192.168.1.1'
	}
}
</pre>

### 撤销DNS
<pre>
{
	'TaskName' : 'OCDN_DEL_DNS',	#Task名字，由于节点故障而撤回DNS
	'Description' : 'del a Node' # Job所描述
	'TaskList' : ['OCDN_DEL_DNS'], #Job所有Task列表
	'CurrentTask': 'OCDN_DEL_DNS', #当前要执行的Task,
	'TimeOut' : 10 #10秒,
	'RunTimesLimit': #Task运行最大次数
	{
		'AlreadyRunTimes': 0,	#当前执行该Task次数
		'MaxRunTimes' : 10 		#最多执行该Task次数
	},
	'Parameters': #参数
	{
		'Node':'192.168.1.1'
	}
}
</pre>
