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
#   Script: tfidf.py
#
#   Processes cleansed tweet .csv files in order to take tweet
#   data and perform TF-IDF analysis
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
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
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
# tweets: a list of all tweet content
#

tweets = []

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
            # Add the tweet's text to the tweets list
            #

            tweets.append(row['text'])

#
# Download stopwords from NLTK - we need them for TF-IDF analysis
#

stopwords_en = stopwords.words('english')

#
# Create TF-IDF vectoriser
#

vectorizer = TfidfVectorizer(max_features=2000, min_df=5, max_df=0.7, stop_words=stopwords_en)

#
# Perform TF-IDF on the tweets using the vectoriser
#

tfidf = vectorizer.fit_transform(tweets).toarray()

#
# Create a DataFrame from the results
#

tfidf_df = pd.DataFrame(tfidf, columns=vectorizer.get_feature_names())

#
# Output the DataFrame to a CSV
#

tfidf_df.to_csv(analysispath + 'tfidf_' + year + '.csv')