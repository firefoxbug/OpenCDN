#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.com

"""Run a job's tasklist in order. 

JobManagero: contorl job run 
"""

class JobManager(object):
	"""Manager a job's tasks run orger

	"""
	def __init__(self, jobjson):
		self.jobjson = jobjson
		self.task_lists = None
		self.CurrentTask = None
		self.Parameters = None
		self.AlreadyRunTimes = None
		self.MaxRunTimes = None

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
			if not self.CurrentTask or not self.task_lists :
				return False
			return True
		except Exception, e:
			print str(e)
			return False

	def get_current_task_to_run(self):
		"""Get current task is goting to run
		
		Return (TaskName<string>, Parameters<list>)
		"""
		return (self.CurrentTask, self.Parameters)

	def get_current_task_parameters(self):
		"""Get current task's parameters

		Return (**args)
		"""
		pass

	def is_job_finished(self):
		"""If current task is the last one in this job

		Return True: means the job is finished or some errors
		Return False: means the job is unfinished
		"""
		if self.CurrentTask == self.task_lists[-1]:
			return True
		else :
			return False

	def set_next_task_to_run(self, parameters=[]):
		"""Valid next task going to run's json

		Return json
		"""
		self.jobjson['CurrentTask'] = self.get_next_task_module_name()
		if not self.jobjson['CurrentTask']:
			return None
		self.jobjson['RunTimesLimit']['AlreadyRunTimes'] = 0
		self.jobjson['Parameters'] = parameters
		return self.jobjson

	def get_next_task_parameters(self):
		"""Set Next task's parameters

		"""
		pass

	def get_next_task_module_name(self):
		"""Get next to run's task module name
		
		Return string type
		eg. OCDN_PUSH_CONF
		"""
		try:
			current_task_index = self.task_lists.index(self.CurrentTask)
			return self.task_lists[current_task_index+1]	
		except Exception, e:
			return None

	def set_run_time_out(self, timeout=30):
		"""Set task run out time, default is 30 s.
		
		"""

	def try_run_current_task_again(self):
		"""run this current task again

		return None: the task run times is exceed
		return Json: the task is going to dispatched again
		"""
		if self.is_task_run_times_exceed():
			return None

		self.increase_task_run_times()
		return self.jobjson

	def is_task_run_times_exceed(self):
		"""If this tasks has been dispatched more then the limits, mark this job failured and 
		do not dispatch again.

		Return True : mark the job failured
		Return False : the job will be dispatched again
		"""
		if self.AlreadyRunTimes >=  self.MaxRunTimes:
			return True
		return False

	def increase_task_run_times(self):
		"""Because this task runed failured, set number 'AlreadyRunTimes' plus 1.
		"""
		self.jobjson['RunTimesLimit']['AlreadyRunTimes'] = self.AlreadyRunTimes + 1

class OcdnJSON(object):
	"""Create job json description"""
	def __init__(self):
		self.json_template = {
			'TaskName' : None,
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

	def create_job_json(self, TaskName, TaskList=[], Parameters=[]):
		self.json_template['TaskName'] = TaskName
		self.json_template['TaskList'] = TaskList
		self.json_template['Parameters'] = Parameters
		self.json_template['CurrentTask'] = TaskList[0]
		return self.json_template
