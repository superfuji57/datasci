import MapReduce
import sys

"""
SQL Join Example in the Simple Python MapReduce Framework

  SELECT * 
  FROM Orders, LineItem 
  WHERE Order.order_id = LineItem.order_id
"""

mr = MapReduce.MapReduce()

def mapper(record):
    # key: order id
    # value: record
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)

def reducer(key, list_of_values):
    # key: order id
    # value: list of records
    orders = []
    line_items = []
    for record in list_of_values:
        if record[0] == 'order':
            orders.append(record)
        elif record[0] == 'line_item':
            line_items.append(record)
    for order in orders:
        for line_item in line_items:
            mr.emit(order + line_item)  

if __name__ == '__main__':
  inputdata = open("data/records.json")
  mr.execute(inputdata, mapper, reducer)