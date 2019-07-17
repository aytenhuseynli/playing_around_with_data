from glob import glob
from collections import defaultdict
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import json
from pprint import pprint
import ast

def readxls(filename):
    xls1 = pd.ExcelFile(filename)
    df1 = pd.read_excel(xls1)
    return df1
# process a set of data files, and get all the fields in the columns list
# def process_set(data_files):
#   # first make a defaultdict for each column
#   # all_years_totals = {}
#   #
#   # for data_file in data_files:
#   #   key = data_file.split('.')[-2]
#   #   print(key)

  #   with open(data_file, 'r', encoding='utf-8') as f:
  #     reader = csv.DictReader(f)
  #     for row in reader:
  #       state = row['State']
  #       student = int(row[value])
  #       totals[state] += student
  #   all_years_totals[key] = totals
  # return all_years_totals

institution_info = glob('institution-data/*.csv')

# columns to process
institution_index = ['Type', 'Sector', 'State']
institution_values = ['#Students|any|enrolled', '#Students|any|opened',' #Teachers|any|opened', '#Teachers|any|enrolled','#Users|any|enrolled' ]
columns = ['Type', 'Sector', 'State','#Students|any|enrolled', '#Students|any|opened',' #Teachers|any|opened', '#Teachers|any|enrolled']

# print(institution_data['2017'])
# print(institution_data['2018'])
# print(institution_data['2019'])

# df = pd.read_csv('institution-data/aca-institution-enrolment-detailed.au.2017.csv')
# pd.set_option('precision', 0)
df = pd.read_csv('institution-data/aca-institution-enrolment-detailed.1557755940.au.0.1451566800.csv')

pd.options.display.float_format = '{:.0f}'.format

def pivot(values, index, groupby):
    try:
        table = pd.pivot_table(df,
                            values= values,
                            index = index,
                            aggfunc=np.sum)
        out = pd.concat([d.append(d.sum().rename((k,'Subtotal' ))) for k, d in table.groupby(groupby)]).append(table.sum().rename(('Grand', 'Total')))
        out.index = pd.MultiIndex.from_tuples(out.index)
        print(out)
    except KeyError:
        pass

def pivot2(values, index):
    try:
        table = pd.pivot_table(df,
                            values= values,
                            index = index,
                            aggfunc=np.sum, fill_value = '0', margins = True, dropna = True, margins_name = 'Grand Total')
        print(table)
    except KeyError:
        pass

pivoted = pivot2(['#Grade 3|any|enrolled', '#Grade 4|any|enrolled', '#Grade 5|any|enrolled', '#Grade 6|any|enrolled', '#Grade 7|any|enrolled', '#Grade 8|any|enrolled'],'State')
flattened = pd.DataFrame(pivoted.to_records())
# type = pivot(['#Students|any|enrolled', '#Teachers|any|enrolled'],['State', 'Type'], 'State')
# type_sector = pivot2('#Users|any|enrolled', 'Type', 'Sector')
# sector_type = pivot2('#Users|any|enrolled', 'Sector', 'Type')
# state_type = pivot2('#Users|any|enrolled', 'State', 'Type')
# state_sector = pivot2('#Users|any|enrolled', 'State', 'Sector')


def readxlssheet(filename, sheet):
    xls1 = pd.ExcelFile(filename)
    df1 = pd.read_excel(xls1, sheet_name = sheet)
    return df1
file1 = readxls('institution-data/aca-institution-enrolment-detailed.1557755940.au.0.1451566800.csv')
# file2 = readxls('Medium engagement.xlsx')
# file3 = readxls('High engagement.xlsx')
# file4 = readxls('school-profile-2017-acara.xlsx')
# file5 = readxlssheet('aca-institution-enrolment-detailed.au.csv.xlsx','Low')
# file6 = readxlssheet('aca-institution-enrolment-detailed.au.csv.xlsx','Medium')
# file7 = readxlssheet('aca-institution-enrolment-detailed.au.csv.xlsx','High')
# file8 = pd.read_csv('aca-contact-participating-teacherss.csv')
# # file9 = pd.read_csv('aca-contact-participating-teachers.1.csv', error_bad_lines=False, comment='#', sep = ',', header=None)
# file10 = readxls('All low engagement teachers.xlsx')
# file12 = readxlssheet('Low engagement-schoolprofile.xlsx','Low')
# file11 = readxls('cyber-teachers.xlsx')
# file13 = readxls('aca-contact-participating-teachers-cyber(no duplicates).xlsx')

def merge(data1, data2, value, output):
    mergedStuff = pd.merge(data1, data2, on=value, how='inner')
    mergedStuff.head()
    new = mergedStuff.drop_duplicates(subset=value, keep=False)
    new.to_excel(f'{output}.xlsx')

# merged1 = merge(file8,file5,'Name', 'Low engagement')
# merged2 = merge(file8,file6,'Name', 'Medium engagement')
# merged3 = merge(file8,file7,'Name', 'High engagement')
# merged4 = merge(file1,file4,'ACARA ID', 'Low engagement-schoolprofile')
# merged5 = merge(file2,file4,'ACARA ID', 'Medium engagement-schoolprofile')
# merged6 = merge(file3,file4,'ACARA ID', 'High engagement-schoolprofile')

# merged7 = merge(file8, file1, 'Name', 'All low engagement teachers')

# merged8 = merge(file11, file10, 'Teacher', 'aca-cyber-teachers(duplicates)')

# stuff = pd.merge(file12,file13, on='Teacher', how='inner')
# stufff = stuff.duplicated()
# print(stufff)

#course_data
def convert_tocsv(input, output):
    df = pd.read_json(input)
    df_csv = df.to_csv(f'{output}.csv', encoding='utf-8', index=False)

# full1 = convert_tocsv('course-data/full/aca-dt-7-bk-geometry')
# full2 = convert_tocsv('course-data/full/aca-dt-7-py-biology-extension')
# full3 = convert_tocsv('course-data/full/aca-dt-7-py-biology')
# full4 = convert_tocsv('course-data/full/aca-dt-56-bk-chatbot')
# full5 = convert_tocsv('course-data/full/aca-dt-56-bk-cookie')
# full6 = convert_tocsv('course-data/full/aca-dt-56-bk-invaders')
# full7 = convert_tocsv('course-data/full/aca-dt-56-bk-turtle')
# full8 = convert_tocsv('course-data/full/aca-dt-78-ar-sound')
# full9 = convert_tocsv('course-data/full/aca-dt-78-js-cookie')
# full10 = convert_tocsv('course-data/full/aca-dt-78-js-invaders')
# full11 = convert_tocsv('course-data/full/aca-dt-78-py-chatbot')
# full12 = convert_tocsv('course-data/full/aca-dt-78-py-turtle')
#
# mini1 = convert_tocsv('course-data/mini/aca-dt-mini-34-bk-tree')
# mini2 = convert_tocsv('course-data/mini/aca-dt-mini-34-bk-variables')
# mini3 = convert_tocsv('course-data/mini/aca-dt-mini-56-bk-invaders')
# mini4 = convert_tocsv('course-data/mini/aca-dt-mini-56-bk-satellite')
# mini5 = convert_tocsv('course-data/mini/aca-dt-mini-78-py-satellite')
# mini6 = convert_tocsv('course-data/mini/aca-dt-mini-bk-microbit-intro')
mini7 = convert_tocsv('course-data/mini/aca-dt-mini-bk-microbit-rocket.json','aca-dt-mini-bk-microbit-rocket')
# mini8 = convert_tocsv('course-data/mini/aca-dt-mini-py-microbit-intro')

import glob

path = r'course-data/full'   # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f) for f in all_files))
df1 = df.to_csv('course-data/full/full-merged.csv', encoding='utf-8', index=False)

df2 = pd.read_csv('full-merged.csv')
print(df2.describe())
#
# histogram_intersection = lambda a, b: np.minimum(a, b).sum().round(decimals=1)
# print(df2.corr(method=histogram_intersection))

writer = ExcelWriter("output.xlsx")

# for filename in glob.glob("/*.xlsx"):
#     excel_file = pd.ExcelFile(filename)
#     (_, f_name) = os.path.split(filename)
#     (f_short_name, _) = os.path.splitext(f_name)
#     for sheet_name in excel_file.sheet_names:
#         df_excel = pd.read_excel(filename, sheet_name=sheet_name)
#         df_excel.to_excel(writer, f_short_name+'_'+sheet_name, index=False)
#
# writer.save()
