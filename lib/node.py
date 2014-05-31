#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN Node module: OpenCDN Node manager, reload CDN nodes.

OpenCDN module instruction : 
	OCDN_RELOAD

Reload API :
	
"""

class Node(object):
	"""OpenCDN Node manager"""
	def __init__(self, arg):
		super(Node, self).__init__()
		self.arg = arg			

class Reload(object):
	"""docstring for Reload"""
	def __init__(self, arg):
		super(Reload, self).__init__()
		self.arg = arg
		nginx_reload_queue.init()

	def nginx_reload_loop():
		while True:
			current_task_json_str = Queue.get_item_from_queue('OCDN_RELOAD')
			jobjson = JobJSON(current_task_json)
			(call_module, **arg) = jobjson.get_current_task_to_run()
			if self.nginx_reload(**arg) == False:
				self.nginx_reload_faliure()
				return False

			jobjson.set_next_task_to_run(parameters)
			Queue.put_item_into_queue('OCDN_RELOAD')


	def nginx_reload():
		"""reolad nginx"""
		pass

	def nginx_reload_faliure():
		"""reolad nginx failed"""
		pass