
|  TaskName           |  含义       
| --------------------|:-------------:
| OCDN_ADD_NODE       | 添加节点
| OCDN_DEL_NODE       | 添加节点
| OCDN_ADD_DOMAIN     | 添加域名
| OCDN_DEL_DOMAIN     | 删除域名
| OCDN_REMOVE_CONF    | 删除配置文件 
| OCDN_SYNC_CONF      | 同步配置文件 
| OCDN_VER_CONF       | 查看配置文件的版本
| OCDN_RELOAD_NODE    | 节点reload
| OCDN_PROXY          | 节点proxy检测
| OCDN_ADD_DNS        | 增加DNS
| OCDN_DEL_DNS        | 撤销DNS
| OCDN_PURGE  		  | 擦除缓存
| OCDN_NODE_MONITOR   | 节点检查检查、配置一致性检查
| OCDN_TASK_DISPATCH  | 根据节点一致性问题分发相应Job
| OCDN_LOOP_TASK  	  | 无尽循环任务,会定时会将TaskList自动提交

### 增加域名
<pre>
{
	'JobName' : 'OCDN_ADD_DOMAIN',	#Job名字
	'Description' : 'add a Domain', # Job所描述
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
	'JobName' : 'OCDN_DEL_DOMAIN',	#Job名字
	'Description' : 'del a Domain', # Job所描述
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
	'JobName' : 'OCDN_ADD_NODE',	#Job名字
	'Description' : 'del a Node', # Job所描述
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
	'JobName' : 'OCDN_DEL_DNS',	#Job名字，由于节点故障而撤回DNS
	'Description' : 'del a Node', # Job所描述
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
		['Node':'192.168.1.1']
	}
}
</pre>

### Purge cache
<pre>
{
	'JobName' : 'OCDN_PURGE',	#Job名字
	'Description' : 'purge a Domain cache',
	'TaskList' : ['OCDN_PURGE'], 
	'CurrentTask': 'OCDN_PURGE', #当前要执行的Task,
	'TimeOut' : 10 #10秒,
	'RunTimesLimit': #Task运行最大次数
	{
		'AlreadyRunTimes': 0,	#当前执行该Task次数
		'MaxRunTimes' : 10 		#最多执行该Task次数
	},
	'Parameters': #参数
	{
		[
			{
				'ip':'192.168.1.1',port':'80','domain':'www.firefoxbug.com',token':'821e57c57e8455e3e809e23df7bb6ce9'
			},
			{
				'ip':'192.168.1.2',port':'80','domain':'www.firefoxbug.com',token':'821e57c57e8455e3e809e23df7bb6ce9'
			}
		]
	}
}
</pre>

###节点健康检查
<pre>
{
	'JobName' : 'OCDN_NODE_CHECKER',	#Job名字
	'Description' : 'Check cdn node healthy and recover Bad node's configurations',
	'TaskList' : ['OCDN_NODE_MONITOR','OCDN_TASK_DISPATCH','OCDN_LOOP_TASK'], 
	'CurrentTask': 'OCDN_NODE_MONITOR', #当前要执行的Task,
	'TimeOut' : 600 #60秒,
	'RunTimesLimit': #Task运行最大次数
	{
		'AlreadyRunTimes': 0,	#当前执行该Task次数
		'MaxRunTimes' : 10 		#最多执行该Task次数
	},
	'Parameters': #参数
	{
        #OLD_OK表示上一次检查的结果,经过OCDN_NODE_MONITOR后，OK->BAD的变成 NEW_BAD;BAD-> OK 变成NEW_OK
        #OCDN_NODE_MONITOR 执行完后 将节点状态的json一次性持久华到DB,以供状态查询
        'NODE_STATUS':[
            'OK': ['192.168.1.1'],
            'BAD':['192.168.1.2'] 
            'NEW_OK':[] 
            'NEW_BAD':[] 
         ],
         #OCDN_TASK_DISPATCH 会找NEW_OK或NEW_BAD的机器，提交相应的Job到相应的Queue 
        'LOOP_SLEEP_TIME':600
         #OCDN_LOOP_TASK 则是Sleep LOOP_SLEEP_TIME 秒后，将本json重新提交到本Queue中
	}
}
</pre>
