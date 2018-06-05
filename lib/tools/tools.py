
#print("tools __name__ = " + __name__ )

import logging
# Pour utiliser le logger commun à tout le projet:
#log = logging.getLogger("main")
# Pour utiliser un logger spécifique à ce fichier : (le définir aussi dans le fichier de conf des logs, si différent du logger root)
log = logging.getLogger(__name__)


def dump(obj):
	for attr in dir(obj):
		print("obj.%s = %s" % (attr, getattr(obj, attr)))


import pprint

# TODO there must be a universal way to pretty print any kind of object...
#      => from what I've seen after a short research, not much!
# @param obj
# @param return boolean return result in a string
def print_obj(obj, return_=False):
	r = ''
	if type(obj) is list or dict:
		log.debug("is instance of list or dict")
		for item in obj:
			r += '\n' + pprint.pformat(vars(item))
	else:
		log.debug("is NOT instance of list")
		r = pprint.pformat(vars(obj))

	if return_:
		return r
	pprint.pprint(r)



def print_matrix(m):
	s = [[str(e) for e in row] for row in m]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print('\n'.join(table))



# Naïve log function
def log_(msg):
	print("LOG: " + msg)



import urllib
def add_get_params(url, params):
	# Add trailing / if necessary:
	if (not url.endswith('/')):
		url += '/'
	return url + '?' + urllib.parse.urlencode(params)



def printList(l):
	print('[%s]' % ', '.join(map(str, l)))



# NOT TESTED
def getClassProperties(cls):

	#return [i for i in cls.__dict__.keys() if i[:1] != '_']
	print("getClassProperties")

	import inspect
	attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
	printList(attributes)
	properties = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]

	printList(properties)
	return properties



def removeCommentsFromSql(sql):
	import sqlparse
	from sqlparse import tokens

	# http://stackoverflow.com/questions/5871791/howto-clean-comments-from-raw-sql-file

	return sqlparse.format(sql, None, strip_comments=True)



def getFieldVal(object, field, case_insensitive=False, raise_excp_if_not_found=False):
	"""
	Return the value for the given field (attribute) of the given object
	:param object:
	:param field:
	:param case_insensitive: look for given field in case insensitive fashion
	:return:
	"""
	try:
		if not case_insensitive:
			ret = vars(object)[field]
		else:
			lower_case_fields = {k.lower(): v for k, v in vars(object).items()}
			ret = lower_case_fields[field.lower()]
	except KeyError:
		if (raise_excp_if_not_found):
			raise Exception("tools.getFieldVal(...): Field [%s] not found in object [%s]" % (field, pprint.pformat(object)))
		else:
			ret = None
	return ret



def isSingleWord(string):
	import re
	return re.match(r'\A\w+\Z', string)



def safeReadDict(dict, key, fail_value=None):
	try:
		return dict[key]
	except KeyError:
		return fail_value



def isNumeric(val):
	"""
	Renvoie vrai si val est float ou int
	:param val:
	:return:
	"""
	try:
		float(val)
		return True
	except ValueError:
		pass

	try:
		int(val)
		return True
	except ValueError:
		pass

	return False