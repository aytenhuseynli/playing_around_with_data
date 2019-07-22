import numpy as np
import pandas as pd
import math
from glob import glob
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def analyse(file):
    """Run a sentiment analysis request on a text."""
    with open(file, 'r', encoding='utf-8') as text:
        for line in text:
            line = line.strip()
            # try:
            client = language.LanguageServiceClient()
            document = types.Document(
                content=line,
                type=enums.Document.Type.PLAIN_TEXT)
            annotations = client.analyze_sentiment(document=document)

          # overall score of the comment
            score = annotations.document_sentiment.score
          # emotional magnitude
            magnitude = annotations.document_sentiment.magnitude

            print(f'Text: {line}')
            print(f'Sentiment: {score}, {magnitude}')
            # except UnicodeEncodeError:
            # pass
analyse('_chat.txt')
