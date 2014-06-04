#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

"""Test for opencdn queue

produce task and put task into gearman server
"""
import sys
import os
parent, bindir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
if os.path.exists(os.path.join(parent, 'lib')):
	sys.path.insert(0, os.path.join(parent, 'lib'))

from ocdn_queue import Producer

class ProducerTest(Producer):
	"""docstring for queue_test"""
	def __init__(self, queue_ip='103.6.222.21', queue_port=4730):
		super(ProducerTest, self).__init__(queue_ip, queue_port)		
		self.task_name = 'ProducerTest'

	def produce_job_loop(self):
		self.producer_connect_queue()
		job2do = {'id':'1', 'data':'hello'}
		self.put_task_into_queue('OCDNQUEUE', job2do, Background=False)

if __name__ == '__main__':
	producer = ProducerTest()
	producer.produce_job_loop()