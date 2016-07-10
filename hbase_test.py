import happybase

# connection = happybase.Connection('ec2-54-89-159-57.compute-1.amazonaws.com')
connection = happybase.Connection('192.168.1.8')
table = connection.table('t1')

table.put('row-key', {'f1:qual1': 'value1', 'f1:qual2': 'value2'})

row = table.row('row-key')

print(row['f1:qual1'])  # prints 'value1'

for key, data in table.rows(['row-key-1', 'row-key-2']):
    print (key, data)  # prints row key and data for each row

for key, data in table.scan(row_prefix='row'):
    print (key, data)  # prints 'value1' and 'value2'

row = table.delete('row-key')
