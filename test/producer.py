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

from OcdnQueue import Producer
from OcdnQueue import Consumer
from OcdnLogger import init_logger
from OcdnJob import OcdnJSON

import pprint 
pp = pprint.PrettyPrinter()

class ProducerTest(Producer):
	"""docstring for queue_test"""
	def __init__(self, queue_ip='103.6.222.21', queue_port=4730):
		super(ProducerTest, self).__init__(queue_ip, queue_port)		
		self.task_name = 'ProducerTest'
		self.logger = init_logger(logfile='producer_test.log', stdout=True)
		self.logger.info('Connect to gearman server %s:%s'%(queue_ip, queue_port))

	def produce_job_loop(self, TaskModule, job2do):
		self.connect_queue()
		self.logger.info('Put task into TaskModule:%s'%(TaskModule))
		self.put_task_into_queue(TaskModule, job2do, Background=False)

def produce_job_tes():
	Consumer.push_task(queue_ip='103.6.222.21', queue_port=4730, queue_name='OCDNQUEUE', data='hello')
	
def purge_test():
	TaskName = 'OCDN_PURGE'
	TaskList = ['OCDN_PURGE']
	Parameters = []
	Parameters.append({'ip':'192.168.1.1','port':'80','domain':'www.firefoxbug.com','token':'821e57c57e8455e3e809e23df7bb6ce9'})
	Parameters.append({'ip':'192.168.1.2','port':'80','domain':'www.firefoxbug.com','token':'821e57c57e8455e3e809e23df7bb6ce9'})
	
	test = OcdnJSON()
	job2do = test.create_job_json(TaskName, TaskList, Parameters)
	pp.pprint(job2do)

	producer = ProducerTest()
	producer.produce_job_loop('OCDN_PURGE', job2do)

				
if __name__ == '__main__':
	purge_test()