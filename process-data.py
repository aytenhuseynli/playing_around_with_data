from glob import glob
from collections import defaultdict
import csv
import matplotlib.pyplot as plt
import numpy as np
from sentiment import process_files

# confidence lookup
confidence = {'5': 'very_confident', '4': 'quite_confident',
              '3': 'neutral', '2': 'not_confident', '1': 'no_confidence'}

# convert the values in a dictionary to percentage
def get_percentage(d):
  total = sum(d.values())
  perctange_dict = {}
  for k, v in d.items():
    pct = (v/total)*100
    perctange_dict[k] = round(pct)
  return perctange_dict

# print each set of data out as a percentage
def print_pct(d, title):
  pct = get_percentage(d)
  print(f'{title}:')
  for k, v in pct.items():
    if k == '':
      k = 'no_response'
    print(f'  {k}: {v}%')
  print()

# process a set of data files, and get all the fields in the columns list
def process_set(data_files, columns):
  data = {}
  # first make a defaultdict for each column
  for c in columns:
    data[c] = defaultdict(int)
  for data_file in data_files:
    with open(data_file, 'r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      for row in reader:
        for c in columns:
          try:
            key = row[c]
            key = confidence.get(key, key)
            data[c][key] += 1
          except KeyError:
            pass
  return data


# data files
pre_data_files = glob('regular-data/*pre*.csv')
post_data_files = glob('regular-data/*post*.csv')
lead_teacher_pre_files = glob('lead-teacher/*ws-pre*.csv')
lead_teacher_post_files = glob('lead-teacher/*ws-post*.csv')

# pre dicts
region_attendance = defaultdict(int)
aitsl_numbers = defaultdict(int)
previous_dt_pl = defaultdict(int)

# pre survey data
for f in pre_data_files:
  with open(f, 'r', encoding='utf-8') as pre_file:
    reader = csv.DictReader(pre_file)
    for row in reader:
      aitsl_numbers[row['aitsl']] += 1

      if row['teach']:
        region_attendance[row['teach']] += 1
      else:
        region_attendance[row['region']] += 1
      if row['previous_digitech_pl_none'] == 'on':
        previous_dt_pl['no'] += 1
      else:
        previous_dt_pl['yes'] += 1

def count_rows(files):
  count = 0
  for file in files:
    with open(file, 'r', encoding='utf-8') as f:
      count += sum(1 for line in f)
  count -= len(files)
  return count

# columns to process
post_data_columns = ['excited', 'improved_confidence', 'improved_knowledge',
                     'improved_resources', 'improved_understanding', 'inspiring', 'learn_to_code']
pre_lead_columns = ['aitsl', 'confidence_abstraction', 'confidence_algorithms', 'confidence_implementation',
                    'confidence_integration', 'confidence_representation', 'confidence_saba', 'confidence_tcc']
post_lead_columns = ['improved_confidence', 'improved_integration', 'improved_knowledge',
                     'improved_resources', 'improved_understanding', 'inspiring',	'learn_to_code']

# post survey data
post_data = process_set(post_data_files, post_data_columns)

# lead teacher data
pre_lead_data = process_set(lead_teacher_pre_files, pre_lead_columns)
post_lead_data = process_set(lead_teacher_post_files, post_lead_columns)


region_attendance = get_percentage(region_attendance)
del region_attendance['']

print(f'pre respondants: {count_rows(pre_data_files)}')
print(f'post respondants: {count_rows(post_data_files)}')
print(f'pre-tcc respondants: {count_rows(lead_teacher_pre_files)}')
print(f'post-tcc respondants: {count_rows(lead_teacher_post_files)}')

def print_chart(data, title, d):
  plt.figure()
  names = data.keys()
  processed_names = []
  for n in names:
    processed_names.append(n.replace("_", " ").capitalize())
  y_pos = np.arange(len(data))
  heights = list(data.values())
  plt.rc('xtick', labelsize=8)
  bars = plt.bar(processed_names, height=heights,
                 color='blue', align='center', alpha=0.5)
  plt.xticks(y_pos, processed_names, rotation='vertical')
  plt.margins(0.2)
  plt.subplots_adjust(bottom=0.5)
  plt.ylabel('Percentage')
  plt.title(title.replace("_", " ").capitalize())
  for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x()+0.2, yval + .05, f'{yval:2}%')
  plt.savefig(f'figures/{d}/{title}.png')
  plt.close()


def plot_all(data, data_columns, d):
  for c in data_columns:
    if '' in data[c].keys():
      del data[c]['']
    pct_data = get_percentage(data[c])
    print_chart(pct_data, c, d)


plot_all(pre_lead_data, pre_lead_columns, 'aca')
plot_all(post_lead_data, post_lead_columns, 'aca')

del aitsl_numbers['']
aitsl_pct = get_percentage(aitsl_numbers)
previous_dt_pl_pct = get_percentage(previous_dt_pl)
print_chart(aitsl_pct, 'AITSL - participants', 'tcc')
print_chart(previous_dt_pl_pct, 'Previous training', 'tcc')
print_chart(region_attendance, 'Regions', 'tcc')
plot_all(post_data, post_data_columns, 'tcc')

