#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN Purge module: purge cdn cache.

OpenCDN module instruction : 
	OCDN_PURGE

Purge API :
	http://node_ip:node_port/ocdn/purge/purge?token=node_token&domain=node_domain
"""

import sys
import os
import time
try:
	import json
except Exception, e:
	import simplejson as json

parent, bindir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
if os.path.exists(os.path.join(parent, 'lib')):
	sys.path.insert(0, os.path.join(parent, 'lib'))

from OcdnQueue import Consumer
from OcdnQueue import Producer
from OcdnLogger import init_logger
from OcdnJob import JobManager
from OcdnTask import RunTask

class Purge(Consumer):
	"""OpenCDN Domain cache Purge

	1. Register task module into Consumer
	2. Start work loop get task from queue
	3. Do task if failed redo it until exceed MaxRunTimes
	4. If task done succuss and job is finished then update mysql
	4. If task done success but job is unfinished then put next running task into queue
	"""
	def __init__(self, queue_ip='103.6.222.21', queue_port=4730):
		self.queue_ip = queue_ip
		self.queue_port = queue_port
		self.CURRENT_TASK_MODULE = 'OCDN_PURGE'
		self.logfile = os.path.join(parent,'logs','%s.log'%(self.CURRENT_TASK_MODULE))
		super(Purge, self).__init__(queue_ip, queue_port, logfile=self.logfile)
		self.logger = init_logger(logfile=self.logfile, logmodule=self.CURRENT_TASK_MODULE, stdout=True)
		self.tasker = RunTask()
		self.taskid = None

	def run(self):
		"""Register callback module and start a worker loop do tasks"""
		self.register_task_callback(self.CURRENT_TASK_MODULE, self.do_task)
		self.start_worker()

	def do_task(self, gearman_worker, job):
		"""run a task may cause 3 results

		1. task excuted failed
		2. task excuted success and the job fished
		3. task excuted success but the job unfished
		"""
		data = job.data
		current_job_json = json.loads(data)
		jobmanager = JobManager(current_job_json)
		self.taskid = jobmanager.get_task_id()
		if not jobmanager.check_job_json_is_ok() :
			self.logger.error('TaskID:%s Parse job json failed. DATA:%s'%(self.taskid, job.data))
			return "False"

		# Get task and parameters to run
		task_name, task_args = jobmanager.get_current_task_to_run()

		# Run task
		if self.purge_node(task_args) == False:
			self.logger.error('TaskID:%s do task failed.'%(self.taskid))
			next_task_json = jobmanager.try_run_current_task_again()
			self.purge_node_failure(next_task_json)
			return "False"

		self.logger.info('TaskID:%s do task success'%(self.taskid))
		# Job is finished
		if jobmanager.is_job_finished():
			self.logger.info('TaskID:%s Job is finished'%(self.taskid))
			self.purge_job_success()
			return "True"

		# Job still has tasks to dispatch
		next_task_json = jobmanager.set_next_task_to_run()
		if not next_task_json :
			self.logger.error('TaskID:%s:[FAILED] Job is unfished but no more task to do'%(self.taskid))
			return "False"
		self.put_task_into_queue(next_task_json['CurrentTask'], next_task_json)
		return "True"

	def purge_node(self, task_args):
		"""run task purge one node cache

		return False: job filed
		return True: job success
		"""
		instance_list = []
		for item in task_args:
			purge_url = 'http://%s:%s/ocdn/purge/purge?token=%s&domain=%s'%(item['ip'], item['port'], item['token'], item['domain'])
			instance_list.append(purge_url)
		result = self.tasker.run(instance_list)
#		print result
		return False

	def purge_node_failure(self, next_task_json):
		"""do with purge one node cache failured, try to dispatch the task again."""
		if not next_task_json :
			error_msg = 'TaskID:%s:[FAILED] Exceed MaxRunTimes, no more task to dispatch'%(self.taskid)
			self.logger.error(error_msg)
		else :
			info_msg = 'TaskID:%s try to redo task. AlreadyRunTimes=%s'%(self.taskid, next_task_json['RunTimesLimit']['AlreadyRunTimes'])
			self.logger.info(info_msg)
			self.put_task_into_queue(next_task_json['CurrentTask'], next_task_json)
		
	def purge_job_success(self):
		"""The purge job is excuted successfully"""
		pass

	def put_task_into_queue(self, queue_name, task_json):
		"""Put a new task json into task queue"""
		self.push_task(self.queue_ip, self.queue_port, str(queue_name), task_json)

if __name__ == '__main__':
	purge = Purge()
	purge.run()