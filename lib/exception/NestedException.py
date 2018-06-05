

class NestedException(Exception):
	"""
	@author fhill
	See unit tests for more info
	"""

	def __init__(self, message='', cause=None):

		# Call the base class constructor with the parameters it needs
		super(NestedException, self).__init__(message)

		# Exception having caused this current exception
		self.cause = cause


	def str_with_causes(self, level=0):
		trcbck = ""
		indent  = '   ' * level
		indent2 = '   ' * (level + 1)

		if isinstance (self.cause, NestedException):
			#print("self.cause is instance of NestedException")
			trcbck = self.cause.str_with_causes(level + 1)
			#print("cause_str" + cause_str)
		else:
			trcbck = indent2 + " - TYPE    = " + str(type(self.cause)) + "\n" + \
							 indent2 + " - MESSAGE = " + str(self.cause)


		return \
			indent + "EXCEPTION:" + "\n" + \
			indent + " - TYPE   : " + str(type(self)) + "\n" + \
			indent + " - MESSAGE: " + super(NestedException, self).__str__() + "\n" + \
			indent + " - PARENT : " + "\n" + trcbck


	def __str__(self):
		return self.str_with_causes()