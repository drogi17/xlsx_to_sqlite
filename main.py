import argparse 
import xlrd
import time
import sys
import modules.colors as colors


from datetime import datetime
from modules.simple_sqlite import DataBase


parser = argparse.ArgumentParser(description='xlsx to sqlite')
parser.add_argument('--output', '-o', help='Ouput file')
parser.add_argument('--input', '-i', help='Input file')
parser.add_argument('--table_name', help='Data Base name')

args = parser.parse_args()
if args.input and args.output:
    input_file = args.input
    output_file = args.output
else:
    print('usage: main.py [-h] [--output OUTPUT] [--input INPUT] [--table_name DB_NAME]')
    sys.exit()

if args.table_name: table_name = args.table_name

time_start = datetime.now().strftime("%H:%M:%S").split(":")

print('Connecting to %s' % (input_file))
rb = xlrd.open_workbook(input_file)
print('[%s]Connected' % (colors.ok_text('OK')))
sheet = rb.sheet_by_index(0)
names = sheet.row_values(0)

print('Connecting to %s' % (output_file))
db = DataBase(output_file)
print('[%s]Connected' % (colors.ok_text('OK')))
ADD_messages_table = 'CREATE TABLE "%s" (' % (table_name)
colubns = ""
print('Getting columns')
for name in names:
    ADD_messages_table += '"%s"  TEXT,\n' % (name)
    colubns += "?, "
colubns = colubns[:len(colubns)-2]
ADD_messages_table = ADD_messages_table[:len(ADD_messages_table)-2]
ADD_messages_table += ");"
print('[%s]Getting columns' % (colors.ok_text('OK')))
try:
    db.request(ADD_messages_table)
except:
    print('[%s]Alredy created: %s' % (colors.error_text('ERROR'), table_name))


incert_r = 'INSERT INTO "%s" (' % (table_name)
for name in names:
    incert_r += '"%s", ' % (name)
incert_r = incert_r[:len(incert_r)-2]
incert_r += ")"
line_num = 1
threads = 0
print("Start conversion\n")
db.commit()
for rownum in range(1, sheet.nrows):
    row = sheet.row_values(rownum)
    data_to_add = """   %s
                        VALUES ( %s );""" % (incert_r, colubns)
    try:
        db.request(data_to_add, row)
    except:
        print('[%s]Incorrect data on line: %s' % (colors.error_text('ERROR'), line_num))
    line_num += 1

db.commit()

print('\n\n[%s]Conversion over' % (colors.ok_text('OK')))
time_end = datetime.now().strftime("%H:%M:%S").split(":")
h_time = int(time_end[0]) - int(time_start[0])
if time_end[1] > time_start[1]: 
    m_time = int(time_end[1]) - int(time_start[1])
else: 
    h_time -= 1
    m_time = (60+int(time_end[1])) - int(time_start[1])
if time_end[2] > time_start[2]: 
    s_time = int(time_end[2]) - int(time_start[2])
else: 
    m_time -= 1
    s_time = (60+int(time_end[2])) - int(time_start[2])
print("Program run time: %s:%s:%s" % (h_time, m_time, s_time))