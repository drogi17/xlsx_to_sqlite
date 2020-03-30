import argparse 
import xlrd
import time
import sys

from modules.sql_request import DataBase
from modules.loading import processbar
import modules.colors as colors

parser = argparse.ArgumentParser(description='xlsx to sqlite')
parser.add_argument('--output', '-o', help='Ouput file')
parser.add_argument('--input', '-i', help='Input file')
parser.add_argument('--db_name', help='Data Base name')

args = parser.parse_args()
if args.input and args.output:
    input_file = args.input
    output_file = args.output
else:
    print('usage: main.py [-h] [--output OUTPUT] [--input INPUT] [--db_name DB_NAME]')
    sys.exit()

if args.db_name: db_name = args.db_name

print('Connecting to %s' % (input_file))
rb = xlrd.open_workbook(input_file)
print('[%s]Connected' % (colors.ok_text('OK')))
sheet = rb.sheet_by_index(0)
names = sheet.row_values(0)

print('Connecting to %s' % (output_file))
db = DataBase(output_file)
print('[%s]Connected' % (colors.ok_text('OK')))
ADD_messages_table = 'CREATE TABLE "%s" (' % (db_name)
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
    print('[%s]Alredy created: %s' % (colors.error_text('ERROR'), db_name))


incert_r = 'INSERT INTO "%s" (' % (db_name)
for name in names:
    incert_r += '"%s", ' % (name)
incert_r = incert_r[:len(incert_r)-2]
incert_r += ")"
line_num = 1
print("\nStart conversion\n\n")
for rownum in range(1, sheet.nrows):
    row = sheet.row_values(rownum)
    data_to_add = """   %s
                        VALUES ( %s );""" % (incert_r, colubns)
    try:
        db.request(data_to_add, row)
    except:
        print('[%s]Incorrect data on line: %s' % (colors.error_text('ERROR'), line_num))
    processbar(line_num, sheet.nrows)
    line_num += 1

print('[%s]Conversion over' % (colors.ok_text('OK')))