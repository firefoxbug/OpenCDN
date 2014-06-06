#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

""" OpenCDN Conf module: Parse opencdn configure file.

Conf file:
	conf/opencdn.conf	
"""

import ConfigParser
import string, os, sys

parent, bindir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
if os.path.exists(os.path.join(parent, 'conf')):
	sys.path.insert(0, os.path.join(parent, 'conf'))

class MyParseConf(object):
	def __init__(self,conf_path):
		self.conf_path = conf_path
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(conf_path)
 
	def get_value(self,section,key,is_bool = False,is_int = False):
		if is_bool and not is_int:
			#bool类型
			value = self.cf.getboolean(section,key)
			print key,":",value,type(value)
			return value
		elif not is_bool and is_int:
			value = self.cf.getint(section,key)
			print key,":",value,type(value)
			return value

		value = self.cf.get(section,key)
		print key,":",value,type(value)
		return value

class OcdnParseConf(object):
	"""docstring for OcdnParseConf"""
	def __init__(self):
		self.conf_path = os.path.join(parent, 'conf/opencdn.conf')
		if not os.path.exists(self.conf_path) :
			print "ERROR: opencdn.conf does not exists."
			sys.exit(255)
		self.mpc = MyParseConf(self.conf_path)

	def get_queue_module(self):
		"""Parse opencdn.conf and get queue ip and queue port"""
		queue_ip = self.mpc.get_value("gearman", "queue_ip")
		queue_port = self.mpc.get_value("gearman", "queue_port", is_int=True)
		print queue_ip, queue_port

		
if __name__ == '__main__':
	parser = OcdnParseConf()
	parser.get_queue_module()
