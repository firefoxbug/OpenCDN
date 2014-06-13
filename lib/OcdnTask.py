#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN Task Moudle: Send url request and get response parallel.

Dependenciys: gevent
Notice: unknow gevent monkey how works

"""
import gevent.monkey
gevent.monkey.patch_all()

import gevent
import urllib2

class RunTask(object):
	"""Run instance parallel"""
	def __init__(self):
		super(RunTask, self).__init__()
		pass

	def fetchurl(self, task_num, url, timeout=5):
		"""Send http request and get response no-blocking

		coroutine dispatched may cause all tasks run time increase, so set 
		'timeout' larger then you expected.
		"""
#		print('Process %s: %s start work' % (task_num, url))
		flag = None
		status = None
		message = None
		try :
			req_obj = urllib2.Request(url)
			response = urllib2.urlopen(req_obj, timeout=timeout)
			status = response.code
#			message = response.read()
			flag = True
		except Exception, e :
			message = str(e)
			flag = False

#		print('Process %s: %s %s' % (task_num, url, status))
		return (task_num, flag, url, status, message)

	def run(self, url_list):
		"""Gevent spawn multiply coroutines to run parallel

		Return tuple contain list : [(ip, status, reason)..]
		eg: [(192.168.1.1, True, None),(192.168.2.2, Flase, 'Timeout')]
		"""
		i = 0
		jobs = []
		for url in url_list :
			jobs.append(gevent.spawn(self.fetchurl, i, url))
			i += 1
		gevent.joinall(jobs)
#		for job in jobs :
#			print job.value
		return [ job.value for job in jobs]

if __name__ == '__main__':
	"""Test gevent"""
	url_list = ['http://107.167.184.223/' for _ in range(0, 200)]
	tasker = RunTask()
	result = tasker.run(url_list)
	res = {'SUCCESS':0, 'FAILED':0}
	for item in result :
		if item[1] :
			res['SUCCESS'] += 1
		else :
			res['FAILED'] += 1
	print 'SUCCESS %s '%(res['SUCCESS'])
	print 'FAILED %s'%(res['FAILED'])
