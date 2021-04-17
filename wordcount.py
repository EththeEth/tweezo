################################################################
#
#   TWEEZO - A set of utility scripts for scraping tweets,
#   processing them and performing analysis
#
#   Developed to support a series of labs and assignments for
#   the CEU Digital Tools course for BA students in the
#   2021-21 academic year.
#
#   By Ethan Danesh
#
################################################################
#
#   Script: wordcount.py
#
#   Processes cleansed tweet .csv files in order to take tweet
#   data and perform the following analysis:
#
#   - Counts of words in the corpus
#   - Histogram of word counts
#   - Word cloud
#
#   Make sure 'dedup.py' has been run on your project's tweet
#   data before calling this script
#
################################################################
#
#   The approach taken in this script (and some parts of the
#   code) are based on class lectures and notes from the
#   CEU Digital Tools course for BA students in the 2020-21
#   academic year.
#
################################################################
#
#   Copyright 2021, Ethan Danesh
#
#   Licensed under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in compliance
#   with the License.
#
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing,
#   software distributed under the License is distributed on an
#   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
#   either express or implied. See the License for the specific
#   language governing permissions and limitations under the
#   License.
#
################################################################

import csv
import pandas as pd
import collections
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import config

#
# Define paths for raw CSV files and analysis files.
#
# The 'raw' subdirectory stores raw scraped tweets in CSV files
#
# The 'analysis' subdirectory stores various data files generated
# in the analysis process including generated graphs etc
#

analysispath = config.basepath + project['key'] + '/analysis/'

#
# Variables to hold data that we need:
#
# words: a list of all lemmatised terms from all tweets
#

words = []

#
# Open 'alltweets_dedup.csv' for reading
#

with open(analysispath + 'alltweets_dedup.csv', newline='') as csvfile:

    #
    # Read the contents of the file into a CSV DictReader
    #

    reader = csv.DictReader(csvfile)

    #
    # Iterate through the rows
    #

    for row in reader:

        #
        # Check if the tweet's date is in the target year
        #

        if row['created_at'].startswith(year):

            #
            # Grab the lemmas as a string of text (which is what comes from the CSV
            # and strip out the leading [' and trailing '] so we can split in the next step
            #
            # In the CSV the field looked like:
            #
            # ['word1','word2', ... ,'wordX']
            #
            # So, the [-2:2] syntax gives us:
            #
            # word1','word2', ... ,'wordX
            #

            lemmas = row['lemmas'][2:-2]

            #
            # Split the lemmas string into a list of words using the following
            # string to split:
            #
            # ','
            #
            # Add the words to the words list
            #

            words = words + lemmas.split('\', \'')

#
# Place the words list in a collections counter to count the frequency of each word in the set
#

counter = collections.Counter(words)

#
# Create a Pandas data frame with columns word and count of each word
# from the counter
#

word_counts = pd.DataFrame(list(counter.items()),columns=['word','count'])

#
# Sort the DataFrame by count in descending order
#

word_counts = word_counts.sort_values(by=['count'], ascending=False)

#
# Make the word column the index for the DataFrame
#

word_counts.index = word_counts['word']

#
# Output the list of word frequencies from the DataFrame in 'wordcount.csv'
#

word_counts.to_csv(analysispath + 'wordcount.csv')

#
# Generate a histogram from the word frequency counts
#

plt.figure(figsize=(75,50))
word_counts['count'].plot.bar()
plt.xlabel('Words')
plt.ylabel('Word count')
plt.savefig(analysispath + 'histogram_' + year + '.png')

#
# Merge the words from the words list into a single string of text
# with spaces separating the words
#

text = " ".join(str(word) for word in words)

#
# Generate a word cloud of max 30 words using this text
#

wordcloud = WordCloud(max_font_size=50, max_words=30, background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bicubic")
plt.axis("off")
plt.savefig(analysispath + 'wordcloud_' + year + '.png')
