import pandas as pd
import glob
import csv
import json
import numpy as np
from pprint import pprint
from datetime import datetime
from pandas.io.json import json_normalize
from collections import OrderedDict

json_data = pd.read_json('aca-microbit-321-go.json')
file = json_data.to_csv('aca-microbit-321-go.csv')

def timestamp_diff(file):
    df = pd.read_csv(file, usecols = ['created_at','user_id', 'status', 'kind'])
    # df = pd.read_csv(file, usecols = [date_column,'user_id', 'status', 'kind'], converters = {'created_at': date2datetime})
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')
    # print(df['created_at'])
    df = df.drop_duplicates(subset = 'user_id')
    df = df.sort_values(by=['created_at'])

    first_time = df.iloc[0, 0]
    # check whether there is 'Passed' status
    if (df['status'] == 'Passed').any():
        first_pass = df.loc[df['status'] == 'Passed', ['created_at']]
        last_time = first_pass.iloc[0, 0]
    # if not, take the last submission
    else:
        last_time = df.created_at.iat[-1]

    df['difference'] = df['created_at'].diff().fillna(0)

    # delta_t_lt1day = df['difference'][df['difference'] < pd.Timedelta(1,'D')]
    # delta_t_lt1hour = df['difference'][df['difference'] < pd.Timedelta(1,'h')]
    delta_t_lt5minute = df['difference'][df['difference'] < pd.Timedelta(5,'m')]

    print(delta_t_lt5minute)

    print(delta_t_lt5minute.mean())

    count_tries_submissions = df.groupby(['status']).size().reset_index(name='count')
    print('count_tries_sumbissions')
    print(count_tries_submissions)

timestamp_diff('aca-microbit-321-go.csv')
