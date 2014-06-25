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

try:
	import json
except Exception, e:
	import simplejson as json
from OcdnLogger import init_logger

import redis

class OcdnQueue(object):
	"""Simple Queue with Redis Backend

	>>> redis_q = RedisQueue(host='127.0.0.1')
	>>> redis_q.put('KEY', 'Value')
	>>> redis_q.get('KEY')
	"""
	def __init__(self, **redis_kwargs):
		"""The default connection parameters are: host='localhost', port=6379, db=0"""
		self.__db= redis.Redis(**redis_kwargs)

	def qsize(self, key):
		"""Return the approximate size of the queue."""
		return self.__db.llen(key)

	def empty(self):
		"""Return True if the queue is empty, False otherwise."""
		return self.qsize() == 0  

	def put(self, key, item):
		"""Put item into the queue."""
		try :
			self.__db.rpush(key, item)
			return True
		except Exception, e :
			return False

	def get(self, key ,block=True, timeout=None):
		"""Remove and return an item from the queue.  

		If optional args block is true and timeout is None (the default), block
		if necessary until an item is available."""
		try :
			if block:
				item = self.__db.blpop(key, timeout=timeout)
			else:
				item = self.__db.lpop(key)  

			if item:
				item = item[1]
			return item
		except Exception, e :
			return None

	def get_keys(self):
		"""Get all queue keys from redis

		return list
		"""
		try:
			return self.__db.keys()
		except Exception, e:
			return []

	def get_info(self):
		"""Get detail queue information"""
		print "%-20s 		%-10s\n"%("Queue", "Size")
		queue_list = self.get_keys()
		for key in queue_list :
			size = self.qsize(key)
			print "%-20s 		%-10s"%(key, size)
			
	def get_nowait(self, key):
		"""Equivalent to get(False)."""
		return self.get(key, block=False)

import gearman
class Producer(object):
	"""OpenCDN Queue control: use gearman manage all tasks queue.

	producer: 
	1. producer need to connect to gearman
	2. produce tasks and put them into queue"""
	def __init__(self, queue_ip='127.0.0.1', queue_port=4730):
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
	def __init__(self, queue_ip='127.0.0.1', queue_port=4730, logfile='consumer.log'):
		self.gearman_server_addr = "%s:%s"%(queue_ip,queue_port)
		super(Consumer, self).__init__([self.gearman_server_addr])
		self.conlog = init_logger(logfile=logfile, logmodule='CONSUMER', stdout=True)

	def register_task_callback(self, queue_name, callback):
		"""Register callback module. once task arrive in the queue the callback 
		will be called and dispatch the task
		"""
		msg = 'TaskModule:%s'%(queue_name)
		try:
			self.register_task(queue_name, callback)
			self.conlog.info('%s: Register task into gearman success'%(msg))
		except Exception, e:
			self.conlog.error('%s: Register task into gearman failed: %s'%(msg))

	def start_worker(self):
		"""Do tasks in a loop"""
		self.work()

	def on_job_execute(self, current_job):
		return super(Consumer, self).on_job_execute(current_job)

	def on_job_exception(self, current_job, exc_info):
		error_msg = 'TaskModule: %s '%current_job.task
		for item in exc_info[1]:
			error_msg += str(item)
		self.conlog.error(error_msg)
		return super(Consumer, self).on_job_exception(current_job, exc_info)

	def on_job_complete(self, current_job, job_result):
#		message = '[SUCCESS] TaskModule: %s '%(current_job.task)
#		self.conlog.info(message)
		return super(Consumer, self).send_job_complete(current_job, job_result)
		
#	@classmethod
	def push_task(self, queue_ip, queue_port, queue_name, data, Background=True):
		"""Connect to queue and put task into queue"""
		try:
			self.gearman_server_addr = "%s:%s"%(queue_ip,queue_port)
			self.producer = gearman.GearmanClient([self.gearman_server_addr])
			self.producer.submit_job(queue_name, json.dumps(data), background=Background)
			self.conlog.info('TaskModule:%s: Put new task into queue success'%(queue_name))
			return True
		except Exception, e:
	#		print str(e)
			self.conlog.error('TaskModule:%s: Put new task into queue. Data:%s'%(queue_name, data))
			return False

if __name__ == '__main__':
	Consumer.push_task(queue_ip='103.6.222.21', queue_port=4730, queue_name='OCDNQUEUE', data='hello')
