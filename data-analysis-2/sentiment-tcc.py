import numpy as np
import pandas as pd
import math
from glob import glob
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyse(comment):
  """Run a sentiment analysis request on a comment."""
  client = language.LanguageServiceClient()

  document = types.Document(
      content=comment,
      type=enums.Document.Type.PLAIN_TEXT)
  annotations = client.analyze_sentiment(document=document)

  # overall score of the comment
  score = annotations.document_sentiment.score
  # emotional magnitude
  magnitude = annotations.document_sentiment.magnitude

  # also run on NLTKs VADER
  sid = SentimentIntensityAnalyzer()
  sentiment = sid.polarity_scores(comment)
  return score, magnitude, sentiment['compound']

def process_files(files, column_to_analyse, output):
  """process a list of files and save the output dataframe"""

  # read all files and concatenate them into a single dataframe
  df = pd.concat((pd.read_csv(f, usecols=[column_to_analyse]) for f in files))
  # drop rows that are NaN in the comments column
  df = df.dropna(axis=0, subset=[column_to_analyse])
  # for each row, run the analyse function, and add the scores and magnitude to new columns in the dataframe
  df['g-score'], df['g-magnitude'], df['nltk-score'] = zip(*df.apply(lambda row: analyse(row[column_to_analyse]), axis=1))
  # save the data as mgspack
  df.to_msgpack(f'{output}.msg')

lead_teacher_post_files = glob('lead-teacher/*ws-post*.csv')
post_data_files = glob('regular-data/*post*.csv')
process_files(lead_teacher_post_files, 'comments', 'tcc-lead-post-data')
process_files(post_data_files, 'comments', 'post-data')