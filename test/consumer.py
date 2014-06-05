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

from OcdnQueue import Consumer
from OcdnLogger import init_logger

class ConsumerTest(Consumer):
	"""docstring for Consumer"""
	def __init__(self, queue_ip='103.6.222.21', queue_port=4730):
		self.task_name = 'CONSUMER'
		self.logfile = os.path.join(parent,'logs','%s.log'%(self.task_name))
		super(ConsumerTest, self).__init__(queue_ip, queue_port, logfile=self.logfile)
		self.logger = init_logger(logfile=self.logfile, logmodule='CONSUMER_TEST', stdout=True)

	def run(self):
		self.logger.info("Start work")
		self.register_task_callback('OCDN_PURGE', self.do_task)
		self.start_worker()

	def do_task(self, gearman_worker, job):
		data = job.data
		parameters = json.loads(data)
		Consumer.push_task(queue_ip='103.6.222.21', queue_port=4730, queue_name='OCDNQUEUE', data=parameters)
		print parameters
		return 'True'

if __name__ == '__main__':
	consumer = ConsumerTest()
	consumer.run()