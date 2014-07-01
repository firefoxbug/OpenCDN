#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN Purge module: purge cdn cache.

OpenCDN module instruction : 
	OCDN_PURGE

1. Get task's json from own moudle task queue.
2. Check task's json synx
Purge API :
	http://node_ip:node_port/ocdn/purge/purge?token=node_token&domain=node_domain
"""

import sys
import os

parent, bindir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
if os.path.exists(os.path.join(parent, 'lib')):
	sys.path.insert(0, os.path.join(parent, 'lib'))

from OcdnJob import JobScheduler
from OcdnTask import RunTask

class Purge(JobScheduler):
	"""OpenCDN Domain cache Purge

	1. Register task module into Redis
	2. Start work loop get task from queue
	3. Do task if failed redo it until exceed MaxRunTimes
	4. If task done succuss and job is finished then update mysql
	4. If task done success but job is unfinished then put next running task into queue
	"""
	def __init__(self):
		self.CURRENT_TASK_MODULE = 'OCDN_DOMAIN'
		super(Purge, self).__init__()
		self.tasker = RunTask()

	def do_task(self):
		"""run task purge one node cache

		return False: job filed
		return True: job success
		"""
		instance_list = []
		for item in self.Parameters:
			purge_url = 'http://%s:%s/ocdn/purge/purge?token=%s&domain=%s'%(item['ip'], item['port'], item['token'], item['domain'])
			instance_list.append(purge_url)
		result = self.tasker.run(instance_list)
		return False

	def do_task_failed(self):
		"""do with purge one node's cache failured, try to dispatch the task again."""
		self.logger.error('JobID:%s Do task failed.'%(self.jobid))
		pass

	def do_task_succss(self):
		"""The purge job is excuted successfully"""
		self.logger.info('JobID:%s Do task success.'%(self.jobid))
		return True


if __name__ == '__main__':
	purge = Purge()
	purge.start_worker()