# from pathlib import Path, PureWindowsPath
#
# # I've explicitly declared my path as being in Windows format, so I can use forward slashes in it.
# filename1 = PureWindowsPath("C:\Users\ahus2540\Documents\movie_data\full-train.txt")
# filename2 = PureWindowsPath("C:\Users\ahus2540\Documents\movie_data\full-test.txt")
# # Convert path to the right format for the current operating system
# correct_path1 = Path(filename1)
# correct_path2 = Path(filename2)
#
# print(correct_path1)
# print(correct_path2)

# prints "source_data/text_files/raw_data.txt" on Mac and Linux
# prints "source_data\text_files\raw_data.txt" on Windows


reviews_train = []
for line in open(r'C:\Users\ahus2540\Documents\movie_data\full-train.txt', encoding = 'utf-8'):
    reviews_train.append(line.strip())

reviews_test = []
for line in open(r'C:\Users\ahus2540\Documents\movie_data\full-test.txt', encoding = 'utf-8'):
    reviews_test.append(line.strip())

#clean the text

import re

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def preprocess_reviews(reviews):
    reviews = [REPLACE_NO_SPACE.sub("", line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(" ", line) for line in reviews]

    return reviews

reviews_train_clean = preprocess_reviews(reviews_train)
reviews_test_clean = preprocess_reviews(reviews_test)
