#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN Conf module: push or remove CDN config files.

OpenCDN module instruction : 
	OCDN_PUSH_CONF
	OCDN_REMOVE_CONF

Purge API :
	
"""

class Conf(object):
	"""OpenCDN CDN Nodes config file manager

	1. push all config files to CDN Nodes.
	2. remove all config files on CDN Nodes.
	"""
	def __init__(self, arg):
		super(OcdnConf, self).__init__()
		self.arg = arg

	def conf_loop():
		while True:
			current_task_json_str = Queue.get_item_from_queue('OCDN_PUSH_CONF')
			jobjson = JobJSON(current_task_json)
			(call_module, **arg) = jobjson.get_current_task_to_run()
			if self.push_cdn_conf(**arg) == False:
				self.push_cdn_conf_failure()
				return False

			jobjson.set_next_task_to_run(parameters)
			Queue.put_item_into_queue('OCDN_RELOAD')

	def push_cdn_conf():
		"""sync nginx config file to all Nodes

		"""

	def push_cdn_conf_failure():
		"""sync config files failed
		"""

	def remove_cdn_conf():
		"""remove nginx config file

		"""

	def remove_cdn_conf_failure():
		"""remove nginx config file failed
 
		"""	