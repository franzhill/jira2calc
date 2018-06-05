"""
 Les tests unitaires du pauvre ... ;o)

 A exécuter directement, de manière autonome

 @python-version 3.3.5
 @author fhill
 @since 2017.01.13

"""



# < Pour pouvoir lancer ce script depuis ici et quand même utiliser tous les autres modules
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '\..\..')
print(sys.path)
# />




from lib.tools.tools import *
import logging.config



logging.config.fileConfig('../../conf/logging.conf')


print("\n\n")
print("#######################################################################")
print("# Testing tools...")
print("#")
print("\n\n")



print("\n\n")
print("#======================================================================")
print("# Test case 1...")
print("\n\n")


assert(    isSingleWord('word') )
assert(not isSingleWord('this is not a word'))
assert(    isSingleWord('this_is_a_word'))
assert(not isSingleWord('this_is_not;a_word'))
assert(not isSingleWord('this_is_nota_word;'))
assert(not isSingleWord("';DROP DATABASE"))