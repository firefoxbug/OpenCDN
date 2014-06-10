#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN Task Moudle: do all tasks from all Task Moudle

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

	def fetchurl(self, task_num, url, Timeout=3):
		"""Send http request and get response no-blocking"""
		print('Process %s: %s start work' % (task_num, url))
		flag = None
		status = None
		error_msg = None
		try :
			req_obj = urllib2.Request(url,timeout=Timeout)
			response = urllib2.urlopen(req_obj, timeout=5)
			status = response.code
			result = response.read()
			flag = True
		except Exception, e :
			error_msg = str(e)
			flag = False

		print('Process %s: %s %s' % (task_num, url, status))
		return (task_num, flag, url, status, error_msg)

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
		for job in jobs:
			print job.value

if __name__ == '__main__':
	url_list = ['http://107.167.184.223/' for _ in range(0, 10)]
	tasker = RunTask()
	tasker.run(url_list)