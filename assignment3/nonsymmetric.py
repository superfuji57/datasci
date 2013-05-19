import MapReduce
import sys
from collections import Counter

"""
Non-Symmetric Friends Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

def mapper(record):
	# key: friend 1
	# value: friend 2
	key = record[0]
	value = record[1]
	mr.emit_intermediate(key, value)
	mr.emit_intermediate(value, key)

def reducer(key, list_of_values):
	# key: person 
	# value: list of other people who has friendship relation with the person
	# output: people having a nonsymmetric relationship
	c = Counter(list_of_values)
	for person in c.elements():
		if c[person] == 1:
			mr.emit((key, person))

# Do not modify below this line
# =============================
if __name__ == '__main__':
	inputdata = open("data/friends.json")
	mr.execute(inputdata, mapper, reducer)
