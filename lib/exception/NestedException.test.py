"""
 Les tests unitaires du pauvre ... ;o)

 A exécuter directement, de manière autonome

 @python-version 3.3.5
 @author fhill
 @since 2017.01.13

 Will output something similar to :

> C:\java\Python33\python.exe "E:/02-COMPUTING/20-PROJECTS/Jira Extraction/CALC/Jira2Calc/lib/exceptions/NestedException.test.py"

#======================================================================
# Testing Nested Exceptions...



#----------------------------------------------------------------------
# Printing a nested exception without traceback:


EXCEPTION:
 - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
 - MESSAGE: As a result of the previous exceptions, we're raising that final exception...
 - PARENT :
   EXCEPTION:
    - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
    - MESSAGE: As a result of the previous exceptions, we're raising this exception...
    - PARENT :
      EXCEPTION:
       - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
       - MESSAGE: Nested exception. We have control here
       - PARENT :
          - TYPE    = <class 'Exception'>
          - MESSAGE = NOT a nested exception on which we do not have control (may be raised by a e.g. lib)



#----------------------------------------------------------------------
# Printing a nested exception WITH traceback:


!!! Une erreur s'est produite :
EXCEPTION:
 - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
 - MESSAGE: As a result of the previous exceptions, we're raising that final exception...
 - PARENT :
   EXCEPTION:
    - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
    - MESSAGE: As a result of the previous exceptions, we're raising this exception...
    - PARENT :
      EXCEPTION:
       - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
       - MESSAGE: Nested exception. We have control here
       - PARENT :
          - TYPE    = <class 'Exception'>
          - MESSAGE = NOT a nested exception on which we do not have control (may be raised by a e.g. lib)

TRACEBACK:
Traceback (most recent call last):
  File "E:/02-COMPUTING/20-PROJECTS/Jira Extraction/CALC/Jira2Calc/lib/exceptions/NestedException.test.py", line 25, in <module>
    raise Exception("NOT a nested exception on which we do not have control (may be raised by a e.g. lib)")
Exception: NOT a nested exception on which we do not have control (may be raised by a e.g. lib)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "E:/02-COMPUTING/20-PROJECTS/Jira Extraction/CALC/Jira2Calc/lib/exceptions/NestedException.test.py", line 27, in <module>
    raise NestedException("Nested exception. We have control here", e)
lib.exceptions.NestedException.NestedException: EXCEPTION:
 - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
 - MESSAGE: Nested exception. We have control here
 - PARENT :
    - TYPE    = <class 'Exception'>
    - MESSAGE = NOT a nested exception on which we do not have control (may be raised by a e.g. lib)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "E:/02-COMPUTING/20-PROJECTS/Jira Extraction/CALC/Jira2Calc/lib/exceptions/NestedException.test.py", line 29, in <module>
    raise NestedException("As a result of the previous exceptions, we're raising this exception...", e)
lib.exceptions.NestedException.NestedException: EXCEPTION:
 - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
 - MESSAGE: As a result of the previous exceptions, we're raising this exception...
 - PARENT :
   EXCEPTION:
    - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
    - MESSAGE: Nested exception. We have control here
    - PARENT :
       - TYPE    = <class 'Exception'>
       - MESSAGE = NOT a nested exception on which we do not have control (may be raised by a e.g. lib)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "E:/02-COMPUTING/20-PROJECTS/Jira Extraction/CALC/Jira2Calc/lib/exceptions/NestedException.test.py", line 31, in <module>
    raise NestedException("As a result of the previous exceptions, we're raising that final exception...", e)
lib.exceptions.NestedException.NestedException: EXCEPTION:
 - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
 - MESSAGE: As a result of the previous exceptions, we're raising that final exception...
 - PARENT :
   EXCEPTION:
    - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
    - MESSAGE: As a result of the previous exceptions, we're raising this exception...
    - PARENT :
      EXCEPTION:
       - TYPE   : <class 'lib.exceptions.NestedException.NestedException'>
       - MESSAGE: Nested exception. We have control here
       - PARENT :
          - TYPE    = <class 'Exception'>
          - MESSAGE = NOT a nested exception on which we do not have control (may be raised by a e.g. lib)




#======================================================================
# Testing Regular (non nested) Exceptions...



#----------------------------------------------------------------------
# Printing exception...:


NOT a nested exception



#======================================================================
# Testing Nested Exception with no cause...



#----------------------------------------------------------------------
# Printing exception...:


Nested exception with no cause

Process finished with exit code 0




"""

import traceback

from lib.exception.NestedException import *

print("\n\n")
print("#======================================================================")
print("# Testing Nested Exceptions...")
print("\n\n")

try:
	try:
		try:
			try:
				raise Exception("NOT a nested exception on which we do not have control (may be raised by a e.g. lib)")
			except Exception as e:
				raise NestedException("Nested exception. We have control here", e)
		except Exception as e:
			raise NestedException("As a result of the previous exception, we're raising this exception...", e)
	except Exception as e:
		raise NestedException("As a result of the previous exception, we're raising that final exception...", e)
except Exception as e:
	print("#----------------------------------------------------------------------")
	print("# Printing a nested exception without traceback: \n\n")
	print(e)

	print("\n\n")
	print("#----------------------------------------------------------------------")
	print("# Printing a nested exception WITH traceback: \n\n")
	print("!!! Une erreur s'est produite : \n" + str(e)  + "\n\n" + "TRACEBACK: \n" + traceback.format_exc() )


print("\n\n")
print("#======================================================================")
print("# Testing Regular (non nested) Exceptions...")
print("\n\n")

try:
	raise Exception("NOT a nested exception")
except Exception as e:
	print("#----------------------------------------------------------------------")
	print("# Printing exception...: \n\n")
	print(e)

print("\n\n")
print("#======================================================================")
print("# Testing Nested Exception with no cause...")
print("\n\n")


try:
	raise Exception("Nested exception with no cause")
except Exception as e:
	print("#----------------------------------------------------------------------")
	print("# Printing exception...: \n\n")
	print(e)



