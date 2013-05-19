import MapReduce
import sys

"""
Inverted Index Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = value.split()
    words = set(words)
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence docids
    
    mr.emit((key, list_of_values))

if __name__ == '__main__':
  inputdata = open("data/books.json");
  mr.execute(inputdata, mapper, reducer)