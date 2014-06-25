#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

"""Test for opencdn queue

produce task and put task into gearman server
"""
import sys
import time
import os
parent, bindir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
if os.path.exists(os.path.join(parent, 'lib')):
	sys.path.insert(0, os.path.join(parent, 'lib'))

from OcdnQueue import OcdnQueue
from OcdnQueue import JsonCheck
from OcdnLogger import init_logger
from OcdnJob import OcdnJSON

import pprint 
pp = pprint.PrettyPrinter()

class ProducerTest():
	"""docstring for queue_test"""
	def __init__(self, queue_ip='my.opencdn.cc', queue_port=6379):
		self.queue = OcdnQueue(queue_ip, queue_port)
		self.task_name = 'ProducerTest'
		self.logfile = os.path.join(parent,'logs','producer.log')
		self.logger = init_logger(logfile=self.logfile, stdout=True)
		self.logger.info('Connect to redis server %s:%s'%(queue_ip, queue_port))

	def produce_job_loop(self, TaskModule, job2do):
		self.logger.info('Put task into TaskModule:%s'%(TaskModule))
		self.queue.put(TaskModule, job2do)

def purge_test():
	JobName = 'OCDN_PURGE'
	TaskList = ['OCDN_PURGE']
	Parameters = []
	Parameters.append({'ip':'192.168.1.1','port':'80','domain':'www.firefoxbug.com','token':'821e57c57e8455e3e809e23df7bb6ce9'})
	Parameters.append({'ip':'192.168.1.2','port':'80','domain':'www.firefoxbug.com','token':'821e57c57e8455e3e809e23df7bb6ce9'})
	
	test = OcdnJSON()
	job2do = test.create_job_json(JobName, TaskList, Parameters)
	pp.pprint(job2do)

	producer = ProducerTest()
	producer.produce_job_loop('OCDN_PURGE', job2do)

def add_domain_test():
	TaskName = 'OCDN_PURGE'
	TaskList = ['OCDN_PURGE','OCDN_PROXY','OCDN_ADD_DNS']
	Parameters = []
	for _ in range(0,10) :
		Parameters.append({'ip':'192.168.1.1','port':'80','domain':'www.firefoxbug.com','token':'821e57c57e8455e3e809e23df7bb6ce9'})
		Parameters.append({'ip':'192.168.1.2','port':'80','domain':'www.firefoxbug.com','token':'821e57c57e8455e3e809e23df7bb6ce9'})
	
	test = OcdnJSON()
	job2do = test.create_job_json(TaskName, TaskList, Parameters)
	pp.pprint(job2do)

	producer = ProducerTest()
	job2do = JsonCheck.encode(job2do)
	if job2do :
		while True:
			time.sleep(1)
			producer.produce_job_loop(TaskName, job2do)

if __name__ == '__main__':
	add_domain_test()