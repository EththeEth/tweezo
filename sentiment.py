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
#   Script: sentiment.py
#
#   Perform sentiment analysis on tweets. Specifically:
#
#   1. Valence over the tweet series including rolling averages
#
#   2. Arousal over the tweet series including rolling averages
#
#   3. Dominance over the tweet series incl rolling averages
#
#   4. A time series analysis of either valence, arousal or
#      dominance over the entire tweet set as a single text
#      corpus of merged tweets in chronological order
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

import pandas as pd
import re
import csv
import spacy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import config

#
# Utility function to calculate average sentiment
# for a block of text
#
# Function takes three arguments:
#
# text: the window of text to process
#
# lexicon: the sentiment data lexicon
#
# label: the name of the column in the lexicon containing
# the sentiment scores we want to use
#

def avg_sentiment(text, lexicon, label):

    #
    #  Create variables to hold a sum and counter
    #

    sent_sum, sent_count = 0, 0

    #
    # Loop through words in the text windows
    #

    for word in text:

        #
        # Check if the word is in the sentiment data
        # lexicon
        #

        if word in lexicon.index:

            #
            # If the word is in the lexicon, add its
            # score to the sum
            #
            # Also increment the counter so we can calculate
            # the average later
            #

            sent_sum += lexicon.loc[word, label]
            sent_count += 1

    #
    # Check if the counter is greater than zero (i.e. we found
    # words to score
    #

    if sent_count:

        #
        # If we have words, calculate the score
        #

        avg_sent = sent_sum / sent_count

    else:

        #
        # If no words, return a non-number (NaN)
        #

        avg_sent = np.nan

    return avg_sent

#
# Utility function to calculate sentiment time
# series for a corpus of text
#
# Function takes three arguments:
#
# corpus: the complete text to process
#
# lexicon: the sentiment data lexicon
#
# label: the name of the column in the lexicon containing
# the sentiment scores we want to use
#
# win_jump: the jump size to use in traversing the corpus
# which defaults to 100 words
#
# win_size: the window size for each window to use in calculating
# sentiment scores which defaults to 100 words
#

def sentiment_tseries(corpus, lexicon, label, win_jump=100, win_size=100):

    #
    # Create a list to hold the time series data
    #

    sent_tseries = []

    #
    # Iterate through the words in the corpus in steps matching the
    # jump size (win_jump)
    #

    for start_pos in range(0, len(corpus), win_jump):

        #
        # Get a window starting at the current position of the specified
        # window size
        #

        text = corpus[start_pos: start_pos + win_size]

        #
        # If the current text window is a complete window then calculate
        # average sentiment and add it to the time series data list
        #

        if len(text) == win_size:
            avg_sent = avg_sentiment(text, lexicon, label)
            sent_tseries.append(avg_sent)

    return sent_tseries

#
# Define paths for analysis files.
#
# The 'analysis' subdirectory stores various data files generated
# in the analysis process including generated graphs etc
#

analysispath = config.basepath + project['key'] + '/analysis/'

#
# Path to sentiment data Warriner et al's project to extend
# the anew lexicon to a large corpus of terms:
#
# http://crr.ugent.be/archives/1003
#
# This lexicon expands the ANEW data in the research of Warriner, A. B.,
# Kuperman, V., & Brysbaert, M. (2013). Norms of valence, arousal,
# and dominance for 13,915 English lemmas. Behavior research methods,
# 45(4), 1191-1207.
#
# The research project makes the lexicon available under the Creative
# Commons Attribution-NonCommercial-NoDerivs 3.0 Unported license
#

warriner = './lexicons/warriner.csv'

#
#   Read in the sentiment data into a DataFrame (DW Zhou sentiment data)
#

sentiment = pd.read_csv(warriner, index_col='Word')

#
# Create list to hold list of tweet words
#

tweets_list = []

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
            # Add the row to the tweets list
            #

            tweets_list.append(row)

#
# Create tweets data frame
#

tweets = pd.DataFrame(tweets_list)

#
# Create lists to store valence, arousal and dominance of the tweet set
#

valence = []
arousal = []
dominance = []

#
# Update the user since the script takes a while
#

print('Calculate valence, arousal and dominance')

#
# Iterate through tweets looking at lemmas columns
# in order to calculate valence, arousal, dominance
#

for tweet in list(tweets['lemmas']):

    #
    # Create dataframe from list of words n tweet
    #

    tweet_words = pd.DataFrame(eval(tweet), columns=['Word'])

    #
    # Calculate sentiment values for words
    #

    result = pd.merge(tweet_words, sentiment, on="Word")

    #
    # Append average values to two decimal points to empty lists created above
    # for valence, arousal and dominance
    #

    valence.append(round(result[["V.Mean.Sum"]].mean(), 2))
    arousal.append(round(result[["A.Mean.Sum"]].mean(), 2))
    dominance.append(round(result[["D.Mean.Sum"]].mean(), 2))

#
# Store the scores for the tweets in the tweets DataFrame
#

tweets['valence'] = valence
tweets['arousal'] = arousal
tweets['dominance'] = dominance

#
# Update the user since the script takes a while
#

print('Calculate valence, arousal and dominance rolling averages')

#
# Calculate rolling averages for valence, arousal and dominance
#
# We will do rolling averages for 3, 5 and 10 tweet windows
#
# Results are added as columns to the tweets DataFrame
#

tweets['valence_rolling_3'] = tweets.valence.rolling(3).mean()
tweets['valence_rolling_5'] = tweets.valence.rolling(5).mean()
tweets['valence_rolling_10'] = tweets.valence.rolling(10).mean()

tweets['arousal_rolling_3'] = tweets.arousal.rolling(3).mean()
tweets['arousal_rolling_5'] = tweets.arousal.rolling(5).mean()
tweets['arousal_rolling_10'] = tweets.arousal.rolling(10).mean()

tweets['dominance_rolling_3'] = tweets.dominance.rolling(3).mean()
tweets['dominance_rolling_5'] = tweets.dominance.rolling(5).mean()
tweets['dominance_rolling_10'] = tweets.dominance.rolling(10).mean()

#
# Save new CSV 'alltweets_sentiment.csv' which includes these
# valence, arousal, and dominance scores along with the rolling
# averages
#

tweets.to_csv(analysispath + 'alltweets_sentiment_' + year + '.csv')

#
# Update the user since the script takes a while
#

print('Generate valence, arousal and dominance graphs')

#
# Plot valence, arousal and dominance graphs
# next to each other in a single PNG
#

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20,4))
ax[0].plot(valence)
ax[0].set_title('Valence')
ax[1].plot(arousal)
ax[1].set_title('Arousal')
ax[2].plot(dominance)
ax[2].set_title('Dominance')
plt.savefig(analysispath + 'sentiment_' + year + '.png')
plt.close()

#
# Update the user since the script takes a while
#

print('Calculate valence, arousal and dominance three-day rolling average graph')

#
# Plot three-day rolling average graphs for valence,
# arousal and dominance in a single graph
#

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20,4))
ax[0].plot(tweets['valence'], data = tweets, label = 'Valence')
ax[0].plot(tweets['valence_rolling_3'], data = tweets, label = '3-day rolling avg')
ax[0].set_title('Valence')
ax[0].legend()

ax[1].plot(tweets['arousal'], data = tweets, label = 'Arousal')
ax[1].plot(tweets['arousal_rolling_3'], data = tweets, label = '3-day rolling avg')
ax[1].set_title('Arousal')
ax[1].legend()

ax[2].plot(tweets['dominance'], data = tweets, label = 'Dominance')
ax[2].plot(tweets['dominance_rolling_3'], data = tweets, label = '3-day rolling avg')
ax[2].set_title('Dominance')
ax[2].legend()
plt.savefig(analysispath + 'sentiment_rolling_3_' + year + '.png')
plt.close()

#
# Update the user since the script takes a while
#

print('Calculate valence, arousal and dominance five-day rolling average graph')

#
# Plot five day rolling average graphs for valence,
# arousal and dominance in a single graph
#

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20,4))
ax[0].plot(tweets['valence'], data = tweets, label = 'Valence')
ax[0].plot(tweets['valence_rolling_5'], data = tweets, label = '5-day rolling avg')
ax[0].set_title('Valence')
ax[0].legend()

ax[1].plot(tweets['arousal'], data = tweets, label = 'Arousal')
ax[1].plot(tweets['arousal_rolling_5'], data = tweets, label = '5-day rolling avg')
ax[1].set_title('Arousal')
ax[1].legend()

ax[2].plot(tweets['dominance'], data = tweets, label = 'Dominance')
ax[2].plot(tweets['dominance_rolling_5'], data = tweets, label = '5-day rolling avg')
ax[2].set_title('Dominance')
ax[2].legend()
plt.savefig(analysispath + 'sentiment_rolling_5_' + year + '.png')
plt.close()

#
# Update the user since the script takes a while
#

print('Calculate valence, arousal and dominance ten-day rolling average graph')

#
# Plot ten day rolling average graphs for valence,
# arousal and dominance in a single graph
#

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20,4))
ax[0].plot(tweets['valence'], data = tweets, label = 'Valence')
ax[0].plot(tweets['valence_rolling_10'], data = tweets, label = '10-day rolling avg')
ax[0].set_title('Valence')
ax[0].legend()

ax[1].plot(tweets['arousal'], data = tweets, label = 'Arousal')
ax[1].plot(tweets['arousal_rolling_10'], data = tweets, label = '10-day rolling avg')
ax[1].set_title('Arousal')
ax[1].legend()

ax[2].plot(tweets['dominance'], data = tweets, label = 'Dominance')
ax[2].plot(tweets['dominance_rolling_10'], data = tweets, label = '10-day rolling avg')
ax[2].set_title('Dominance')
ax[2].legend()
plt.savefig(analysispath + 'sentiment_rolling_10_' + year + '.png')
plt.close()

#
# Let's load Spacy ready for the next analysis
#
# To use Spacy this way we first need to prepare for it:
#
# 1. Install spacy, for instance:
#
# conda install spacy
#
# 2. At the command prompt download the en_core_web_sm data set:
#
# python -m spacy download en_core_web_sm
#

nlp = spacy.load('en_core_web_sm')
nlp.max_length = 2000000

#
# Let's create a corpus string to store the content of all tweets
# in chronological order in a string to generate a sentiment time
# series of valence on the whole corpus of tweets
#
# We start with reversing the order of the tweets and creating
# a raw corpus string of all tweet content -- order is reversed
# because our CSV is reverse chronological order
#

corpus_raw = ''

for idx in reversed(tweets.index):
    corpus_raw = corpus_raw + str(tweets.loc[idx, 'text']) + '\n'

#
# Remove extra white space, lowercase all words
#

corpus_re = re.sub( r'\W+', ' ', corpus_raw ).lower().strip()

#
# Create a Spacy object
#

corpus_nlp = nlp(corpus_re)

#
# Delete stopwords and lemmatise the full corpus
#

corpus = [w.lemma_ for w in corpus_nlp if nlp.vocab[w.text].is_stop == False if len(w) > 1]

#
# Update the user since the script takes a while
#

print('Generate full corpus time series scores and graph for ' + metric)

#
# To get the right column we need to derive the column name from the chosen metric:
#
# 1. Get the first character of the metric name (for instance, "v")
#
# 2. Capitalise it (for instance, "V")
#
# 3. Append ".Mean.Sum" (for instance, "V.Mean.Sum")
#

metric_column = metric[0].upper() + '.Mean.Sum'

#
# Generate the sentiment time series data based on Valence Mean scores
# from the warriner.csv sentiment lexicon data set
#

win_size = 500
win_jump = 100
sent_tseries = sentiment_tseries(corpus, sentiment, metric_column, win_jump=win_jump, win_size=win_size)

#
# Plot the time series graph
#

xplot = np.linspace(0, 1, len(sent_tseries) + 1)[1:] * 100
yplot = sent_tseries

plt.plot(xplot, yplot)

plt.xlabel('Progress through Tweets (Window: ' + str(win_size) + ', Jump: ' + str(win_jump) + ')')
plt.ylabel('Average ' + metric)

plt.savefig(analysispath + metric + '_timeseries_' + year + '.png')
plt.close()

#
# Update the user since the script takes a while
#

print('Generate comparative sensitivity analysis graph for ' + metric)

#
# Supplement the time series with a comparative analysis
# of time series graphs for different window and jump
# sizes:
#
# 100, 300 and 500 for jump sizes
# 500, 1000, 2000 and 5000 for window sizes
#
# We start by creating two lists to specify the range
# of window and jump sizes to use

win_jump_vals = [10, 100, 1000]
win_size_vals = [500, 1000, 2000, 5000]

#
# Prepare to plot a 3 x 3 grid of graphs for comparative analysis
#

fig = plt.figure(figsize=(12, 8))  # Set up figure
grid = gridspec.GridSpec(len(win_jump_vals), len(win_size_vals), hspace=0.7, wspace=0.4)  # Set up a grid based on length of lists above

#
# Loop through jump sizes list
#

for jump_pos, win_jump in enumerate(win_jump_vals):

    #
    # Loop through window sizes list
    #

    for size_pos, win_size in enumerate(win_size_vals):

        #
        # Keep the user informed because this process takes a while
        #

        print('window jump = {}, window size = {}'.format(win_jump, win_size))

        #
        # Calculate sentiment time series for the specified jump and window sizes
        #

        sent_tseries = sentiment_tseries(corpus, sentiment, metric_column, win_jump=win_jump, win_size=win_size)

        #
        # Add the time series graph to the grid
        #

        ax = plt.subplot(grid[jump_pos, size_pos])

        xplot = np.linspace(0, 1, len(sent_tseries) + 1)[1:] * 100  # x-axis: percentage of corpus
        yplot = sent_tseries  # y-axis: sentiment time series

        plt.plot(xplot, yplot)  # plot time series

        #
        # Add title and labels
        #

        plt.title('window jump = {}\nwindow size = {}'.format(win_jump, win_size))

        if jump_pos == len(win_jump_vals):

            #
            # Only label column at the very bottom of the grid -- not in every graph
            #
            # We check this by comparing the current position in the list to the length
            # of the list -- make sure we are at the list entry
            #

            plt.xlabel('percentage of tweets')  # axis labels

        if size_pos == 0:

            #
            # Only label the rows at the very left of the grid -- not in every graph
            #
            # We check this by comparing the current position in the list to check it
            # is the first entry in the list
            #

            plt.ylabel('average\n' + metric)

#
# Save the completed grid of graphs
#

plt.savefig(analysispath + metric + '_timeseries_sensitivity_' + year + '.png')
plt.close()
