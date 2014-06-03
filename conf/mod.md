各个模块参数和功能
================

# 模块

* OCDN_MODIFI_DNS 生效DNS记录
函数依赖: 通信
传入参数: subDomain, ip
业务逻辑: 

* OCDN_DEL_DNS
函数依赖: 无
传入参数: subDomain, ip or record_id
业务逻辑: 

* OCDN_SYNC_CONF 同步配置文件
函数依赖: 通信
传入参数: config, file, ip, token

* OCDN_DEL_CONF 删除配置文件
函数依赖: 通信
传入参数: file, ip, token

* OCDN_MAKE_CONF 生成配置文件
函数依赖: db
传入参数: domain

* OCDN_VER_CONF 检查配置文件版本
函数依赖: 通信
传入参数: domain, ip, version

* OCDN_TRAFFIC 通信模块
函数依赖: 无
传入参数: http包(method,url,data...)

* OCDN_DOMAIN_STATUS 域名状态更新
函数依赖: db
传入参数: domain, status(normal,complete,deleting,delete)
业务逻辑: 控制数据库domain记录变更状态
返回值: nodes

* OCDN_NODE_RELOAD 节点reload
函数依赖: 通信
传入参数: ip, token

* OCDN_DOMAIN_NODE 域名节点状态更新
函数依赖: db
传入参数: domain, ip, status(new,complete,fault,delete)

* OCDN_NODE_STATUS 节点状态更新
函数依赖: db
传入参数: ip, status(normal, fault, deleting, delete)
业务逻辑: 控制数据node记录变更状态
返回值: domains

* OCDN_NODE_HEART 节点检测
函数依赖: 通信
传入参数: ip, token

# 任务

* ADD_DOMAIN
** OCDN_DOMAIN_STATUS(domain, status=normal) -> get nodes
** OCDN_MAKE_CONF(domain)
** OCDN_SYNC_CONF(config, file, ip, token)
** OCDN_NODE_RELOAD(ip, token) -> (No) retry..
** OCDN_VER_CONF(domain, ip, version) -> (No) retry..
** OCDN_MODIFI_DNS(subDomain, ip) -> (No) retry..
** OCDN_DOMAIN_STATUS(domain, status=complete)

* REMOVE_DOMAIN
** OCDN_DOMAIN_STATUS(domain, status=deleting) -> get nodes
** OCDN_DEL_DNS(subDomain, ip) -> (No) retry..
** OCDN_DEL_CONF(file, ip, token) -> (No) retry..
** OCDN_DOMAIN_NODE(domain, ip, status=delete)
** OCDN_DOMAIN_STATUS(domain, status=delete)

* ADD_NODE
** OCDN_NODE_HEART(ip, token)
** OCDN_NODE_STATUS(ip, status=normal)

* REMOVE_NODE
** OCDN_NODE_STATUS(ip, status=deleting) -> get domains
** OCDN_DEL_DNS(suDomain, ip) -> (No) retry..
** OCDN_DEL_CONF(file, ip, token) -> (No) retry..
** OCDN_DOMAIN_NODE(domain, ip, status=delete)
** OCDN_NODE_STATUS(ip, status=delete)

* FAULT_NODE 当一个节点故障
** OCDN_NODE_STATUS(ip, status=fault) -> get domains
** OCDN_DEL_DNS(suDomain, ip) -> (No) retry..

* RECOVER_NODE 当一个节点恢复
** OCDN_NODE_STATUS(ip) -> get domains
** OCDN_SYNC_CONF(config, file, ip, token)
** OCDN_MODIFI_DNS(suDomain, ip) -> (No) retry..
** OCDN_NODE_STATUS(ip, status=normal)

* JOIN_NODE 把一个节点加入一个已经在运行的CDN域名
** OCDN_DOMAIN_NODE(domain, ip, status=new)
** OCDN_SYNC_CONF(config, file, ip, token)
** OCDN_MODIFI_DNS(suDomain, ip) -> (No) retry..
** OCDN_DOMAIN_NODE(domain, ip, status=complete)



