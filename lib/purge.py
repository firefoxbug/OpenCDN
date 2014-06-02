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

class Purge(object):
	"""OpenCDN Domain cache Purge"""
	def __init__(self, arg):opencdn
		super(Purge, self).__init__()
		self.arg = arg
		self.CURRENT_TASK_MODULE = 'OCDN_PURGE'
		purge_queue.init()
	
	def purge_loop():
		"""run a task may cause 3 results

		1. task excuted failed
		2. task excuted success and the job fished
		3. task excuted success but the job unfished
		"""
		while True:
			current_task_json_str = Queue.get_task_from_queue(self.CURRENT_TASK_MODULE)
			jobjson = JobJSON(current_task_json)

			# Get task and parameters to run
			(call_module, **arg) = jobjson.get_current_task_to_run()

			# Run task
			if self.purge_node(**arg) == False:
				self.purge_node_failure()
				continue

			# Job is over
			if jobjson.is_job_finished():
				self.purge_job_success()
				continue

			# Job still has tasks to dispatch
			next_task_json = jobjson.set_next_task_to_run(parameters)
			next_task_module = jobjson.get_next_task_module_name()
			if next_task_module:
				Queue.put_task_into_queue(next_task_json)

	def purge_node():
		"""run task purge one node cache

		return False: job filed
		return True: job success
		"""

	def purge_node_failure():
		"""do with purge one node cache failured, try to dispatch the task again.

		"""

		next_task_json = jobjson.try_run_current_task_again()
		if next_task_json:
			Queue.put_task_into_queue(self.CURRENT_TASK_MODULE)

	def purge_job_success():
		"""The purge job is excuted successfully
		"""