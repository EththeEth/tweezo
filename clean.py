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
#   Script: clean.py
#
#   Processes raw tweet .csv files in order to remove
#   punctuation and peform other cleansing and then
#   create new .csv files in another directory
#
#   We store two things:
#
#   1. a cleansed version of each tweet in the 'cleaned'
#      subdirectory
#   2. a merged file with all cleansed tweets in the 'analysis'
#      subdirectory
#
#   These cleansed CSV files will contain six columns:
#
#   - tweet_id: The Twitter ID of the tweet
#
#   - created_at: Publication date of the tweet
#
#   - text: Cleansed content of the tweet
#
#   - words: A list of words in the tweet
#
#   - stopwords: A list of words excluding stopwords in the
#                tweet
#
#   - lemmas: A lemmatised list of terms in the tweet
#
#   Typically this script should run immediately after
#   scraping tweets with 'init.py' or 'scrape.py'
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

import string
import re
import csv
import os
import nltk
from nltk.corpus import stopwords
import config

#
# Define paths for raw CSV files and cleansed CSV files.
#
# The 'raw' subdirectory stores raw scraped tweets in CSV files
#
# The 'cleaned' subdirectory stores cleansed CSV files
#
# The 'analysis' subdirectory stores various data files generated
# in the analysis process including generated graphs etc
#

rawpath = config.basepath + project['key'] + '/raw/'
cleanpath = config.basepath + project['key'] + '/cleaned/'
analysispath = config.basepath + project['key'] + '/analysis/'

#
# Utility function to remove URL from text
#
# We use a regular express to perform the URL removal
#
# The function takes one argument:
#
# txt: A string of text to perform URL removal on
#
# The function returns a string containing the source
# string after URLs have been removed
#

def remove_url(txt):

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


#
# Download stopwords from NLTK -- we are using the standard
# NLTK English stopwords list
#

stopwords_en = stopwords.words('english')

#
# Add custom stopwords to the stop word list
#

for stopword in project['stopwords']:
    stopwords_en.append(stopword)

#
# Download and instantiate the NLTK WordNet lemmatiser
#

nltk.download('wordnet')
wn = nltk.WordNetLemmatizer()

#
# Open 'alltweets.csv' in the analysis directory to hold
# the complete set of cleansed tweets ready for analysis
#
#

with open(analysispath + 'alltweets.csv', 'w') as f:

    allwriter = csv.writer(f)
    allwriter.writerow(['tweet_id', 'created_at', 'text', 'words', 'stopwords', 'lemmas'])

    #
    # Get list of raw CSV files and sort alphanumerically
    #

    filelist = os.listdir(rawpath) # Get all files in target directory
    filelist.sort() # Sort files alphanumerically

    #
    # Loop through file list and and cleanse each raw file
    #

    for filename in filelist:

        #
        # Make sure it is a CSV file (just in case)
        #

        if re.search('\.csv$', filename): # Check if file name is .csv

            #
            # Determine file name for cleansed CSV output file
            #

            cleanfile = cleanpath + filename

            #
            # Output some info for the user to keep them posted on progress
            #

            print('Processing file: ' + filename)

            #
            # Create empty objects to hold a list of tweet text and tweet
            # creation dates
            #

            tweets = {}
            tweets_dates = {}

            #
            # Open the raw CSV file for reading
            #

            with open(rawpath + filename, newline='') as csvfile:

                #
                # Create a CSV DictReader to read the file
                #

                reader = csv.DictReader(csvfile)

                #
                # Loop through rows in the CSV and read in the tweet text and dates
                # Using the Tweet ID as the keys in the 'tweets' and 'tweet_dates'
                # objects
                #

                for row in reader:
                    tweets[row['tweet_id']] = row['text']
                    tweets_dates[row['tweet_id']] = row['created_at']

            #
            # Create empty objects to hold various processed data:
            #
            # tweet_lemmas: holds lemmas of words in a tweet
            # tweet_words: holds list of words in a tweet
            # tweet_clean: holds cleansed text of tweets
            # tweet_stopwords: holds cleansed text of tweets without stopwords
            #
            # The tweet ID will be the key in each object
            #

            tweet_lemmas = {}
            tweet_words = {}
            tweet_clean = {}
            tweet_stopwords = {}

            #
            # Loop through every tweet to perform a whole bunch of work
            #

            for tweet_id in tweets:

                #
                # Get the tweet's text and remove URLs
                #

                text = remove_url(tweets[tweet_id])

                #
                # Strip out punctuation by iterating through each character
                # and making sure it isn't in a standard list of punctuation
                #

                text = "".join([char for char in text if char not in string.punctuation]) # Strip punctuation

                #
                # Remove numbers from the tweet text
                #

                text = re.sub('[0-9]+', '', text) # For the time being we don't want to remove numbers

                #
                # Standardise the text to lowercase
                #

                text = text.lower()

                #
                # Store the cleansed text in tweet_clean
                #

                tweet_clean[tweet_id] = text

                #
                # Store the list of words in the tweet in tweet_words
                #
                # We get the list of words by just using split() to
                # split into words
                #

                tweet_words[tweet_id] = text.split()

                #
                # Store the list of words without stopwords in tweet_stopwords
                #
                # We remove stopwords by iterating through each word in tweet_words
                # and comparing to the list of NLTK stopwords we downloaded
                #

                tweet_stopwords[tweet_id] = [word for word in tweet_words[tweet_id] if word not in stopwords_en]

                #
                # Define an empty list in tweet_lemmas for the list of lemmatised words
                # in the tweet
                #

                tweet_lemmas[tweet_id] = []

                #
                # Loop through the list of words (excluding stopwords) and add
                # the lemmatised word to the list in tweet_lemmas
                #
                # We lemmatise the word with the lemmatiser we instantiated earlier
                # in 'wn'
                #
                # append() is used to add each lemmatised term to the list
                #

                for word in tweet_stopwords[tweet_id]:
                    tweet_lemmas[tweet_id].append(wn.lemmatize(word))

            #
            # Open the matching CSV in the 'cleaned" subdirectory for writing
            #

            with open(cleanfile, 'w') as fi:

                #
                # Prepare to write to the file with the CSV module
                #

                writer = csv.writer(fi)
                writer.writerow(['tweet_id', 'created_at', 'text', 'words', 'stopwords', 'lemmas'])

                #
                #   Loop through tweet_clean to get each tweet and write
                #   out all six data points
                #

                for tweet_id in tweet_clean:
                    writer.writerow([tweet_id, tweets_dates[tweet_id], tweet_clean[tweet_id], tweet_words[tweet_id], tweet_stopwords[tweet_id], tweet_lemmas[tweet_id]])


            # Loop through tweet_clean again and this time write out
            # rows into the 'alltweets.csv' file for our merged tweet file
            #

            for tweet_id in tweet_clean:
                allwriter.writerow([tweet_id, tweets_dates[tweet_id], tweet_clean[tweet_id], tweet_words[tweet_id], tweet_stopwords[tweet_id], tweet_lemmas[tweet_id]])
