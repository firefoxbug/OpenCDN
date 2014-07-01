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

parent, bindir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
if os.path.exists(os.path.join(parent, 'lib')):
	sys.path.insert(0, os.path.join(parent, 'lib'))

from OcdnJob import JobScheduler

class ConsumerTest(JobScheduler):
	"""docstring for Consumer"""
	def __init__(self):
		self.CURRENT_TASK_MODULE = 'OCDN_PURGE'
		super(ConsumerTest, self).__init__()
				
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
	consumer.start_worker()