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
from ocdn_log import init_logger
try:
	import json
except Exception, e:
	import simplejson as json

class OCDNQueue(gearman.GearmanWorker):
	"""OpenCDN Queue control: use gearman manage all tasks queue.

	producer: produce tasks and put them into queue
	consumer: get tasks from queue and dispatch them
	"""
	def __init__(self):
		self.logger = init_logger(logfile='ocdn_queue.log')
		self.producer = None
		self.consumer = None

	def producer_connect_queue(self, queue_ip='127.0.0.1', queue_port=4730):
		"""Producer try to connect to gearman server"""
		try :
			gearman_server_addr = "%s:%s"%(queue_ip,queue_port)
			self.producer = gearman.GearmanClient([gearman_server_addr])
		except Exception,e:
			self.logger.error('Producer connect Gearman failured: %s'%(str(e)))
			sys.exit(1)

	def put_task_into_queue(queue_name, data, background=True):
		"""Put a task into a queue"""
		self.producer.submit_job(queue_name,json.dumps(data),background)

	def consumer_connect_queue(self, queue_ip='127.0.0.1', queue_port=4730):
		"""Consumer try to connect to gearman server"""
		try :
			gearman_server_addr = "%s:%s"%(queue_ip,queue_port)
			self.consumer = gearman.GearmanWorker([gearman_server_addr])
		except Exception,e:
			self.logger.error('consumer connect Gearman failured: %s'%(str(e)))
			sys.exit(1)

	def register_task(self, queue_name, callback_func):
		self.consumer.register_task(queue_name, callback_func)

	def start_worker(self):
		"""Do tasks in a loop"""
		self.consumer.work()

	def on_job_execute(self, current_job):
		return super(CustomGearmanWorker, self).on_job_execute(current_job)

	def on_job_exception(self, current_job, exc_info):
		error_msg = '%s ERROR '%current_job.task
		for item in exc_info[1]:
			error_msg += str(item)
		self.logger.error(error_msg)
		return super(CustomGearmanWorker, self).on_job_exception(current_job, exc_info)

	def on_job_complete(self, current_job, job_result):
		message = '%s SUCCESS'%(current_job.task)
		self.logger.info(message)
		return super(CustomGearmanWorker, self).send_job_complete(current_job, job_result)