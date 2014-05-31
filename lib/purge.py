#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN Purge module: purge cdn cache.

OpenCDN module instruction : 
	OCDN_PURGE

Purge API :
	http://node_ip:node_port/ocdn/purge/purge?token=node_token&domain=node_domain
"""

class Purge(object):
	"""OpenCDN Domain cache Purge"""
	def __init__(self, arg):opencdn
		super(Purge, self).__init__()
		self.arg = arg
		purge_queue.init()
	
	def purge_loop():
		while True:
			task = purge_queue.get()
			task.run()
