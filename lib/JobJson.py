
class JobJSON(object):
	""" parse job json 

	"""
	def __init__(self, arg):
		super(JobJSON, self).__init__()
		self.jobjson = jobjson
		self.next_task = None
		self.task_lists = []
		self.CurrentTask = None

	def get_task_lists():
		""" Get all tasks is going to run in a job

		Return a list compose of all tasks
		eg. [OCDN_ADD_DOMIAN, OCDN_PUSH_CONF, OCDN_PROXY]
		"""

	def get_current_task_parameters():
		"""Get current task's parameters

		Return (**args)
		"""

	def get_current_task_to_run():
		"""Get current task is goting to run
		
		Return (TaskName,**args)
		"""
	def get_next_task_parameters():
		"""Set Next task's parameters

		"""

	def get_next_task_module_name():
		"""Get next to run's task module name
		
		Return string type
		eg. OCDN_PUSH_CONF
		"""
		current_task_index = self.task_lists.index(self.CurrentTask)
		next_task_to_run = self.task_lists[current_task_index+1]
		return next_task_to_run

	def set_next_task_to_run(parameters=None):
		"""Valid next task going to run's json

		Return json
		"""

		self.jobjson['CurrentTask'] = self.get_next_task_module_name()
		self.jobjson['RunTimesLimit']['AlreadyRunTimes'] = 0
		self.jobjson['Parameters'] = parameters
		return self.jobjson
		
	def is_job_finished():
		"""If current task is the last one in this job

		Return True: means the job is finished
		Return False: means the job is unfinished
		"""
		if self.CurrentTask == self.task_lists[-1]:
			return True
		else :
			return False

	def set_run_time_out(timeout=30):
		"""Set task run out time, default is 30 s.
		
		"""

	def try_run_current_task_again():
		"""run this current task again

		return None: the task run times is exceed
		return Json: the task is going to dispatched again
		"""
		if self.is_task_run_times_exceed():
			return None

		self.increase_task_run_times()
		return self.jobjson

	def is_task_run_times_exceed():
		"""If this tasks has been dispatched more then the limits, mark this job failured and 
		do not dispatch again.

		Return True : mark the job failured
		Return False : the job will be dispatched again
		"""
		if self.jobjson['AlreadyRunTimes'] >=  self.jobjson['MaxRunTimes']:
			return True
		return False

	def increase_task_run_times():
		"""Because this task runed failured, set number 'AlreadyRunTimes' plus 1.
		"""
		self.jobjson['AlreadyRunTimes'] += 1
