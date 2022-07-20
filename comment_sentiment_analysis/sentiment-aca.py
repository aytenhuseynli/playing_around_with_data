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

df = pd.read_msgpack('aca-post-data.msg')

columns_sent = ['question','comment','g-score','g-magnitude','nltk-score']

# table1 = df.groupby('g-score')['comment'].\
#         agg({'commentcount': pd.Series.nunique})

# table1.plot.barh(align = 'center')

plt.subplots_adjust(left=0.2)
plt.margins(0.3)
plt.ylabel('Sentiment Score')
# plt.show()
# plt.savefig('sentiment_comment.png')

# df.groupby('g-score')['comment'].\
    # agg({'commentcount': pd.Series.nunique,
         # 'comment': lambda x: '|-|'.join(x)}, as_index = False, axis='columns')

df = pd.read_csv('report1.csv')
# f = lambda x: len(x["comment"].split("great")) -1
# df["great"] = df.apply(f, axis=1)

# print(df)
# print(df.loc[df['g-score'] <= 0])
# print(df.loc[df['g-score'] >= 0])
# df = df.set_index(['g-score'])
# print(df.loc[df.index.isin(['0.9'])])

# file = open('report1.csv', encoding="utf8")
file = open('challenge-evaluation-2019.results.2019-03-28.csv', encoding="utf8")
reader = file.read()
# Stopwords
stopwords = set(line.strip() for line in open('stopwords.txt'))
# stopwords = stopwords.union(set(['mr','mrs','one','two','said']))
# Instantiate a dictionary, and for every word in the file,
# Add to the dictionary if it doesn't exist. If it does, increase the count.
wordcount = defaultdict(int)
# To eliminate duplicates, remember to split by punctuation, and use case demiliters.
for word in reader.lower().split():
    word = word.replace(".","")
    word = word.replace(",","")
    word = word.replace(":","")
    word = word.replace("\"","")
    word = word.replace("!","")
    word = word.replace("â€œ","")
    word = word.replace("â€˜","")
    word = word.replace("*","")
    word = word.replace("|-|","")
    if word not in stopwords:
        wordcount[word] += 1
print('finished replacing stuff')
# Print most common word
n_print = 50
word_counter = Counter(wordcount)
print('starting word count')
for word, count in word_counter.most_common(n_print):
    print(word, ": ", count)
print('finished word count')
# Close the file
file.close()
# Create a data frame of the most common words
# Draw a bar chart
lst = word_counter.most_common(n_print)
df = pd.DataFrame(lst, columns = ['Word', 'Count'])
df.plot.bar(x='Word',y='Count')
