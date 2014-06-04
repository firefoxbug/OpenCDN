#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN task queue module: manage all tasks queue.

Queue Task Name:

| OCDN_ADD_NODE     | 添加节点
| OCDN_DEL_NODE     | 添加节点
| OCDN_ADD_DOMAIN   | 添加域名
| OCDN_DEL_DOMAIN   | 删除域名
| OCDN_REMOVE_CONF  | 删除配置文件
| OCDN_SYNC_CONF    | 同步配置文件
| OCDN_VER_CONF     | 查看配置文件的版本
| OCDN_RELOAD_NODE  | 节点reload
| OCDN_PROXY        | 节点proxy检测
| OCDN_ADD_DNS      | 增加DNS
| OCDN_DEL_DNS      | 撤销DNS
| OCDN_PURGE  		| 擦除缓存

"""
import sys
import gearman
try:
	import json
except Exception, e:
	import simplejson as json

class Producer(object):
	"""OpenCDN Queue control: use gearman manage all tasks queue.

	producer: 
	1. producer need to connect to gearman
	2. produce tasks and put them into queue"""
	def __init__(self, queue_ip='127.0.0.1', queue_port=4730):
#		self.logger = init_logger(logfile='producer.log', stdout=True)
		self.gearman_server_addr = "%s:%s"%(queue_ip,queue_port)
		self.producer =None

	def connect_queue(self):
		"""Producer try to connect to gearman server"""
		self.producer = gearman.GearmanClient([self.gearman_server_addr])

	def put_task_into_queue(self, queue_name, data, Background=True):
		"""Put a task into a queue"""
		self.producer.submit_job(queue_name, json.dumps(data), background=Background)

class Consumer(gearman.GearmanWorker):
	"""OpenCDN Queue control: use gearman manage all tasks queue.
	
	consumer: 
	1. consumer need to register into gearman
	2. get tasks from queue and dispatch them
	"""
	def __init__(self, queue_ip='127.0.0.1', queue_port=4730):
		self.gearman_server_addr = "%s:%s"%(queue_ip,queue_port)
		super(Consumer, self).__init__([self.gearman_server_addr])
#		self.logger = init_logger(logfile='consumer.log', stdout=True)

	def register_task_callback(self, queue_name, callback):
		"""Register callback module. once task arrive in the queue the callback 
		will be called and dispatch the task
		"""
		try:
			self.register_task(queue_name, callback)
		except Exception, e:
			error_msg = 'TaskModule:%s Callback:%s'%(queue_name, callback)
			self.logger.error('Register task into gearman failed: %s'%(error_msg))

	def start_worker(self):
		"""Do tasks in a loop"""
		self.work()

	def on_job_execute(self, current_job):
		return super(Consumer, self).on_job_execute(current_job)

	def on_job_exception(self, current_job, exc_info):
		error_msg = '[FAILED] TaskModule: %s '%current_job.task
		for item in exc_info[1]:
			error_msg += str(item)
		self.logger.error(error_msg)
		return super(Consumer, self).on_job_exception(current_job, exc_info)

	def on_job_complete(self, current_job, job_result):
		message = '[SUCCESS] TaskModule: %s '%(current_job.task)
		self.logger.info(message)
		return super(Consumer, self).send_job_complete(current_job, job_result)
		
	@classmethod
	def push_task(self, queue_ip, queue_port, queue_name, data, Background=True):
		"""Connect to queue and put task into queue"""
		try:
			self.gearman_server_addr = "%s:%s"%(queue_ip,queue_port)
			self.producer = gearman.GearmanClient([self.gearman_server_addr])
			self.producer.submit_job(queue_name, json.dumps(data), background=Background)
			return True
		except Exception, e:
			print "ERROR %s"%(str(e))
			return False
			
if __name__ == '__main__':
	Consumer.push_task(queue_ip='103.6.222.21', queue_port=4730, queue_name='OCDNQUEUE', data='hello')