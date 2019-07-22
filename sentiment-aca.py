import numpy as np
import pandas as pd
import math
from glob import glob
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyse(comment, client, sid):
  """Run a sentiment analysis request on a comment."""
  document = types.Document(
      content=comment,
      type=enums.Document.Type.PLAIN_TEXT)
  annotations = client.analyze_sentiment(document=document)

  # overall score of the comment
  score = annotations.document_sentiment.score
  # emotional magnitude
  magnitude = annotations.document_sentiment.magnitude

  # also run on NLTKs VADER
  
  sentiment = sid.polarity_scores(comment)
  print(score, magnitude, sentiment)
  return score, magnitude, sentiment['compound']

def process_files(files, columns_to_analyse, output):
  """process a list of files and save the output dataframe"""
  print('reading files')
  client = language.LanguageServiceClient()
  sid = SentimentIntensityAnalyzer()
  # read all files and concatenate them into a single dataframe
  df = pd.concat((pd.read_csv(f, usecols=columns_to_analyse) for f in files))
  # combine the df so all the comments are in the one column, call 'comment'
  df = df.melt(value_vars=columns_to_analyse, value_name='comment', var_name='question')
  # drop rows that are NaN in the comments column
  df = df.dropna(axis=0, subset=['comment'])
  # for each row, run the analyse function, and add the scores and magnitude to new columns in the dataframe
  df['g-score'], df['g-magnitude'], df['nltk-score'] = zip(*df.apply(lambda row: analyse(row['comment'], client, sid), axis=1))
  # save the data as msgpack
  df.to_msgpack(f'{output}.msg')

aca_post_files = ['aca/aca-post-workshop.results.2019-01-29.csv']
aca_pre_files = ['aca/aca-pre-workshop.results.2019-01-29.csv']
columns = ['comments_day1_activities','comments_day1_info','comments_day2_programming_activities','comments_day2_workshop_lectures']
process_files(aca_post_files, columns, 'aca-post-data')
process_files(aca_pre_files, columns, 'aca-pre-data')

