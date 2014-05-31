
class JobJSON(object):
	""" parse job json 

	"""
	def __init__(self, arg):
		super(JobJSON, self).__init__()
		self.current_task = None
		self.next_task = None
		
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

	def set_next_task_to_run(parameters):
	"""Valid next task going to run's json

	Return json
	"""

	def set_run_time_out(timeout=30):
	"""Set task run out time, default is 30 s.
	
	"""
		

