OpenCDN
=======

Purge
------
* 模块功能

删除指定节点下指定域名的cache

OpenCDN Purge模块: purge.py

* Purge API :

http://node_ip:node_port/ocdn/purge/purge?token=node_token&domain=node_domain

* 请求参数

|  变量        |  含义       
| ----------- |:-------------:
| node_ip     | 节点IP
| node_port   | 端口80或者9242      
| node_token  | 节点token
| node_domain | purge的域名

* 示例:

http://192.168.1.1:80/ocdn/purge/purge?token=node_token&domain=ocdn.me

* 返回参数参考

Proxy
-----
* 模块功能

  1. 检测域名反向代理是否生效
  2. 驱动DNS处理模块

OpenCDN Proxy模块: proxy.py

* Proxy检测 API :

http://node_ip/node_path

示例:



* 请求参数

|  变量        |  含义       
| ----------- |:-------------:
| node_ip     | 节点IP
| node_path   | 检测路径     

* 返回参数参考

DNS
---
* 模块功能

  1. 使得DNS失效或者撤销DNS配置

OpenCDN DNS模块: 

* Proxy检测 API :



示例:



* 请求参数

|  变量        |  含义       
| ----------- |:-------------:
| node_ip     | 节点IP
| node_path   | 检测路径     

* 返回参数参考


## 守护模块
Heartbeat
----
* 模块功能

  1. 检测所有Node健康状态

OpenCDN heartbeat模块: 

* Heartbeat检测 API :

http://node_ip:node_port/ocdn/status?token=node_token


* 请求参数

|  变量        |  含义       
| ----------- |:-------------:
| node_ip     | 节点IP
| node_port   | 端口80或者9242      
| node_token  | 节点token  

* 示例:

http://192.168.1.1:80/ocdn/status?token=node_token

* 返回参数参考


FLOW
----
* 模块功能

  1. 获取所有Node上域名流量

OpenCDN flow模块: 

* Flow检测 API :


示例:


* 请求参数

|  变量        |  含义       
| ----------- |:-------------:
| node_ip     | 节点IP
| node_port   | 端口80或者9242      
| node_token  | 节点token

* 返回参数参考

