
|  TaskName         |  含义       
| ----------------- |:-------------:
| OCDN_ADD_DOMAIN   | 添加节点
| OCDN_DEL_DOMAIN   | 删除节点
| OCDN_PUSH_CONF    | 分发配置文件
| OCDN_REMOVE_CONF  | 删除配置文件 
| OCDN_RELOAD       | 节点reload
| OCDN_PROXY        | 节点proxy检测
| OCDN_ADD_DNS      | 增加DNS
| OCDN_DEL_DNS      | 撤销DNS
| OCDN_PURGE  		| 擦除缓存

{
	'TaskName' : 'ADD_DOMAIN',	#Task名字
	'Description' : 'add a Domain' # Job所描述
	'TaskList' : ['OCDN_PUSH_CONF','OCDN_RELOAD','OCDN_PROXY','OCDN_DNS'], #Job所有Task列表
	'CurrentTask': 'OCDN_PUSH_CONF', #当前要执行的Task,
	'TimeOut' : '10' #10秒
	'Parameters': #参数
	{
		'Domain':'www.firefoxbug.com',
		'Node':'192.168.1.1'
	}
}