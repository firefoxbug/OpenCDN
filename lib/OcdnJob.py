#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

"""Run a job's tasklist in order. 

JobManagero: contorl job run 
"""
import time
import random
from OcdnQueue import OcdnQueue
try:
	import json
except Exception, e:
	import simplejson as json

class JobManager(object):
	"""Manager a job's tasks run 

	"""
	def __init__(self, queue_ip='my.opencdn.cc', queue_port=6379, logger=None):
		self.queue_ip = queue_ip
		self.queue_port = queue_port
		
		self.logger = logger

		self.jobjson = None
		self.task_lists = None
		self.CurrentTask = None
		self.Parameters = None
		self.AlreadyRunTimes = None
		self.MaxRunTimes = None

		self.connect_queue()

	def connect_queue(self) :
		"""Connect to redis queue"""
		self.logger.info("Connecting to redis ip:%s port:%s"%(self.queue_ip,
			self.queue_port))
		self.queue = OcdnQueue(self.queue_ip, self.queue_port)

	def get_job_info(self, queue_name):
		"""Get job to run"""
		if not self.get_job_from_queue(queue_name) :
			return False

		return self.check_job_json_is_ok()

	def get_job_from_queue(self, queue_name):
		"""Get job description json from redis queue"""
		self.jobid = self.get_job_id()
		self.logger.info("Create a job ID:%s"%self.jobid)
		current_job_json = None
		try :
			data = self.queue.get(queue_name)
			self.jobjson = self.decode(data)
		except Exception, e:
			self.logger.error("JobID:%s Get job json from queue:%s failed"%(self.jobid,
				queue_name))
			return False

		if  self.jobjson :
			self.logger.info("JobID:%s Get job json from queue:%s"%(self.jobid, 
				queue_name))
			return True
		else :
			return False

	def put_job_into_queue(self, queue_name, task_json):
		"""Put a new task json into task queue"""
		task_json = self.encode(task_json)
		self.queue.put(str(queue_name), task_json)
		self.logger.info('JobID:%s Put new task into Module:[%s] '%(self.jobid, 
			str(queue_name)))

	def check_job_json_is_ok(self):
		"""Check the job json file syntax is ok or not

		return True  if the json is ok
		return False if the json is error
		"""
		try:
			self.CurrentTask = self.jobjson['CurrentTask']
			self.task_lists = self.jobjson['TaskList']
			self.Parameters =  self.jobjson['Parameters']
			self.AlreadyRunTimes = int(self.jobjson['RunTimesLimit']['AlreadyRunTimes'])
			self.MaxRunTimes = int(self.jobjson['RunTimesLimit']['MaxRunTimes'])
			if not self.CurrentTask :
				self.logger.error("JobID:%s Parse json failed. No CurrentTask in json."%(
					self.jobid))
				return False
			self.logger.info("JobID:%s Parse json success."%self.jobid)
			return True
		except Exception, e:
			self.logger.error("JobID:%s Parse json failed: %s"%(self.jobid, 
				str(e)))
			return False

	def get_job_id(self):
		"""Generate a Job ID

		return <string>(YearMonthDayHourMinuteSecond)
		"""
		return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+str(random.randint(0,10))

	def try_run_next_task(self, parameters=[]):
		"""Check is job over and do left tasks"""
		if self.is_job_finished():
			self.logger.info('JobID:%s Job is finished'%(self.jobid))
			return True

		self.logger.info('JobID:%s Job is unfinished, still has task to do.'%(self.jobid))

		try :
			current_task_index = self.task_lists.index(self.CurrentTask)
			self.jobjson['CurrentTask'] = self.task_lists[current_task_index+1]
			self.jobjson['RunTimesLimit']['AlreadyRunTimes'] = 0
			self.jobjson['Parameters'] = parameters
		except Exception, e:
			self.logger.error("JobID:%s compose next job json failed. %s"%(
				self.jobid, str(e)))
			return False

		self.put_job_into_queue(self.jobjson['CurrentTask'], self.jobjson)
		return True

	def try_run_current_task_again(self):
		"""run this current task again

		return None: the task run times is exceed
		return Json: the task is going to dispatched again
		"""
		if self.is_task_run_times_exceed():
			error_msg = 'JobID:%s Exceed MaxRunTimes, failed to retry dispatch'%(self.jobid)
			self.logger.error(error_msg)
			return False

		self.jobjson['RunTimesLimit']['AlreadyRunTimes'] = self.AlreadyRunTimes + 1

		info_msg = 'JobID:%s Try to redo task. AlreadyRunTimes=%s'%(self.jobid, 
			self.jobjson['RunTimesLimit']['AlreadyRunTimes'])
		self.logger.info(info_msg)

		self.put_job_into_queue(self.jobjson['CurrentTask'], self.jobjson)

	def get_current_task_to_run(self):
		"""Get current task is goting to run
		
		Return (TaskName<string>, Parameters<list>)
		"""
		return (self.CurrentTask, self.Parameters, self.jobid)

	def is_job_finished(self):
		"""If current task is the last one in this job

		Return True: means the job is finished or some errors
		Return False: means the job is unfinished
		"""
		if self.CurrentTask == self.task_lists[-1]:
			return True
		else :
			return False

	def get_next_task_parameters(self):
		"""Set Next task's parameters

		"""
		pass

	def set_run_time_out(self, timeout=30):
		"""Set task run out time, default is 30 s.
		
		"""

	def is_task_run_times_exceed(self):
		"""If this tasks has been dispatched more then the limits, mark this job failured and 
		do not dispatch again.

		Return True : mark the job failured
		Return False : the job will be dispatched again
		"""
		if self.AlreadyRunTimes >=  self.MaxRunTimes:
			return True
		return False

	def encode(self, data) :
		"""Json encode data"""
		try:
			return json.dumps(data)
		except Exception, e:
			raise e
			return None

	def decode(self, data) :
		"""Json decode data"""
		try:
			return json.loads(data)
		except Exception, e:
			raise e
			return None

class OcdnJSON(object):
	"""Create job json description"""
	def __init__(self):
		self.json_template = {
			'JobName' : None,
			'Description' : 'OpenCDN',
			'TaskList' : [], 
			'CurrentTask': None, 
			'TimeOut' : 10,
			'RunTimesLimit': 
			{
				'AlreadyRunTimes': 0,
				'MaxRunTimes' : 10
			},
			'Parameters':{

			}
		}

	def create_job_json(self, JobName, TaskList=[], Parameters=[]):
		self.json_template['JobName'] = JobName
		self.json_template['TaskList'] = TaskList
		self.json_template['Parameters'] = Parameters
		try:
			self.json_template['CurrentTask'] = TaskList[0]
		except Exception, e:
			return None
		
		return self.json_template
