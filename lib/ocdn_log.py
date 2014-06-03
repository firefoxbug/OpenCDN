#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import logging 
 
"""
log level:
	NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
 
	logging.DEBUG
	logging.INFO
	logging.WARNING
	logging.ERROR
	logging.CRITICAL
"""
 
def init_logger(logfile='test.log', stdout=True):
	formatter = logging.Formatter('%(levelname)s [%(asctime)s] %(name)s:%(pathname)s line=%(lineno)d [message="%(message)s"]') 

	logger = logging.getLogger('mylogger') 
	logger.setLevel(logging.INFO) 

	# write log into file
	fh = logging.FileHandler(logfile) 
	fh.setLevel(logging.INFO) 
	fh.setFormatter(formatter) 
	logger.addHandler(fh) 

	if stdout:
		# print log to stdout
		ch = logging.StreamHandler() 
		ch.setLevel(logging.INFO) 
		ch.setFormatter(formatter) 
		logger.addHandler(ch)
	return logger
 
if __name__ == '__main__':
	logger = init_logger(logfile='debug.log', stdout=False)
	logger.info('this is a info log')
	try:
		print 1/0
	except Exception, e:
		logger.error(str(e[0]))
