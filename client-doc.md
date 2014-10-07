# OpenCDN Client 标准接口 1.0

- 所有的信息全部固化在sqlite中
- 操作存在队列的概念，每次只有一个在进行执行
- 所有操作接口皆为全量接口

## 标准输出

	{"code": 0, "result": []}

- version 获取接口版本
- status 当前CDN状态
	- webserver/cacheserver/apps/domains/activeLeft/
- notify 通知(如果用户不传入callback,则信息全部放入通知中) 默认最多1000条
	- notify/marks 传入id来标记消息已读
	- notify/gets 按照id来进行读取
	- notify/limit 按照偏移值来进行读取
	
- systems 获取所有系统信息
	- systems/gets 按照key来获取多项系统信息
		- system/cpu 获取系统CPU信息
		- system/load 获取系统负载信息
		- system/networks	获取系统网卡信息
		- system/time 获取系统时间
- configs 获取所有配置信息
	- configs/gets 按照key来获取多项配置信息
	- configs/updates 配置批量更新 JSON
	- configs/limit 用start,limit来获得配置信息
		- config/webserver web服务器
			- path web服务器路径
			- name web服务器软件名称 nginx/tengine/haproxy/ats/lighted/apache
		- config/apps 应用
			- activeTime 应用生效时间，如果为0，则是立即生效
		- config/cacheserver 缓存服务器
			- path 缓存服务器路径
			- name 缓存服务器软件名称 squid/varnish/nginx_proxy
- apps 获取所有应用名
	- apps/gets 获取指定appName的应用
	- apps/exists 查找是否存在 
	- apps/limit 用start,limit来获得应用信息
	- apps/deletes 应用批量删除 JSON
	- apps/updates 应用批量更新 JSON
	- apps/inserts 应用批量添加 JSON
		- app/appName 获取应用信息
		- app/appName/aliases 获取/更改 应用的别名 ["www.baidu.com", "www.taobao.com"]
		- app/appName/sources 获取/更改 应用的源站 [{"address":"1.1.1.1:81", "host": ""}]
		- app/appName/caches 获取/更改 应用的缓存策略 [{"type": "suffix", ""},]
- actions 
	- actions.start CDN服务启动
	- actions.stop CDN服务停止
	- actions.restart CDN服务重启
	- actions.refresh 全局刷新配置文件并自动reload
	

## web

管理界面
