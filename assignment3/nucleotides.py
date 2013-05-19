import MapReduce
import sys

"""
String trimming Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: sequence id
    # value: nucleotide string
    key = record[0]
    value = record[1]
    mr.emit_intermediate(value[:-10], key)

def reducer(key, list_of_values):
    # key: trimmed seq
    # value: list of dna seq ids which have the same string
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open("data/dna.json")
  mr.execute(inputdata, mapper, reducer)
