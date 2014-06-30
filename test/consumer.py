#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

"""Test for opencdn queue

consumer: get task from gearman server and do task
"""
import sys
import os
import time
import json

parent, bindir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
if os.path.exists(os.path.join(parent, 'lib')):
	sys.path.insert(0, os.path.join(parent, 'lib'))

from OcdnLogger import init_logger
from OcdnJob import JobManager

class ConsumerTest(JobManager):
	"""docstring for Consumer"""
	def __init__(self, queue_ip='my.opencdn.cc', queue_port=6379):
		self.task_name = 'OCDN_PURGE'
		self.logfile = os.path.join(parent,'logs','%s.log'%(self.task_name))
		self.logger = init_logger(logfile=self.logfile, logmodule=self.task_name
			, stdout=True)
		super(ConsumerTest, self).__init__(queue_ip, queue_port, self.logger)

	def run(self):
		while True:
			time.sleep(1)
			if self.get_job_info(self.task_name) :
				if self.do_task() :
					self.do_task_succss()
					self.try_run_next_task()
				else :
					self.do_task_failed()
					self.try_run_current_task_again()
				
	def do_task(self):
		print (self.CurrentTask, self.Parameters, self.jobid)
		return True

	def do_task_succss(self):

		self.logger.info('JobID:%s Do task success.'%(self.jobid))
		return True

	def do_task_failed(self):
		self.logger.error('JobID:%s Do task failed.'%(self.jobid))
		pass

if __name__ == '__main__':
	consumer = ConsumerTest()
	consumer.run()