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
#   Script: compare.py
#
#   Generate proportion shift and sentiment shift graphs for
#   two tweet corpora
#
#   Copies of the graphs will be saved in both your project's
#   'analysis/' directory for reference
#
#   Make sure 'dedup.py' has been run on both projects' tweet
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
import spacy
import csv
import shifterator as sh
import collections as co
import config

#
# Define paths for analysis files.
#
# The 'analysis' subdirectory stores various data files generated
# in the analysis process including generated graphs etc
#

analysispath1 = config.basepath + shift[0] + '/analysis/'
analysispath2 = config.basepath + shift[1] + '/analysis/'

#
# Create object to hold the corpora for the analysis
#

corpora = {}

#
# Let's load Spacy ready for the this analysis
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
# Iterate through the two projects to compare and create corpora
#

for key in shift:

    #
    # Get the relevant project
    #

    project = config.projects[key]

    #
    # Analysis path for this project
    #

    analysispath = config.basepath + key + '/analysis/'

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
    # Store the corpus in the corpora object
    #
    corpora[key] = corpus

#
# Define reference/comparison corpus texts as specified in Config
#

corpus_ref = corpora[shift[0]]
corpus_com = corpora[shift[1]]

#
# Get word frequencies from the corpora
#

corpus_ref_freq = dict(co.Counter(corpus_ref).most_common())
corpus_com_freq = dict(co.Counter(corpus_com).most_common())

#
# Specify the number of words to display in shift graphs
#

top_n = 50

#
# Compute proportion shift object using shifterator
#

proportion_shift = sh.ProportionShift( type2freq_1=corpus_ref_freq,
                                       type2freq_2=corpus_com_freq )

#
# Generate proportion shift graph and save in first project
#
# File name is based on the two project keys for clarity
#

proportion_shift.get_shift_graph( top_n=top_n,
                                  system_names=[shift[0], shift[1]],
                                  show_plot=False,
                                  filename=analysispath1 + shift[0] + '_' + shift[1] + '_proportion_' + year + '.png',
                                  title='Proportion Shift: ' + shift[0] + ', ' + shift[1])

#
# Generate again and sav e in second project
#
# File name is based on the two project keys for clarity
#

proportion_shift.get_shift_graph( top_n=top_n,
                                  system_names=[shift[0], shift[1]],
                                  show_plot=False,
                                  filename=analysispath2 + shift[0] + '_' + shift[1] + '_proportion_' + year + '.png',
                                  title='Proportion Shift: ' + shift[0] + ', ' + shift[1])

#
# Prepare to generate a sentiment shift graph by
# by specifying the sentiment lexicon, the
#

sent_lex = 'labMT_English' # Sentiment lexicon
sent_ref = 5 # (arbitrary) Reference value for sentiment regimes
sent_int = [(4,6)] # Interval of sentiment scores to consider

#
# Compute sentiment shift object
# We use the LabMT sentiment lexicon (included in Shifterator)
#

sentiment_shift = sh.WeightedAvgShift(type2freq_1=corpus_ref_freq,
                                       type2freq_2=corpus_com_freq,
                                       type2score_1=sent_lex,
                                       reference_value=sent_ref,
                                       stop_lens=sent_int)

#
# Generate sentiment shift graph and save in first project
#
# File name is based on the two project keys for clarity
#

sentiment_shift.get_shift_graph(top_n=top_n, detailed=True,
                                system_names=[shift[0], shift[1]],
                                show_plot=False,
                                filename=analysispath1 + shift[0] + '_' + shift[1] + '_sentiment_' + year + '.png',
                                title='Sentiment Shift: ' + shift[0] + ', ' + shift[1])

#
# Generate sentiment shift graph and save in second project
#
# File name is based on the two project keys for clarity
#

sentiment_shift.get_shift_graph(top_n=top_n, detailed=True,
                                system_names=[shift[0], shift[1]],
                                show_plot=False,
                                filename=analysispath2 + shift[0] + '_' + shift[1] + '_sentiment_' + year + '.png',
                                title='Sentiment Shift: ' + shift[0] + ', ' + shift[1])

