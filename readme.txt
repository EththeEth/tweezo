################################################################
#
#   TWEEZO - A set of utility scripts for scraping tweets,
#   processing them and performing analysis
#
#   Developed to support a series of labs and assignments for
#   the Central European University Digital Tools course for BA
#   students in the 2021-21 academic year.
#
#   By Ethan Danesh
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

#
# DESCRIPTION
#

This project is a set of utility scripts for scraping tweets, processing them and performing a range of analysis
on corpora of tweets scraped with the scripts. The types of analysis these scripts product include:

- Counts of words in the corpus
- Histogram of word counts
- Word cloud
- TF-IDF analysis
- Valence scores over a series of tweets including rolling averages
- Arousal scores over a series of tweets including rolling averages
- Dominance scores over a series of tweets including rolling averages
- Time series analysis of valence over a corpora of merged tweet text from a series of tweets
- Proportion shift and sentiment shift graphs to compare two tweet corpora

At this time, the scripts only work with user timeline searches using the Twitter API's 'user_timeline' method.

#
# DEPENDENCIES
#

Before using the scripts there are some dependencies you will need. The scripts use the following Python modules:

- tweepy
- csv
- os
- pandas
- nltk
- nltk.corpus
- collections
- matplotlib
- matplotlib.pyplot
- matplotlib.gridspec
- wordcloud
- sklearn.feature_extraction.text
- string
- re
- spacy
- shifterator
- networkx
- itertools
- gensim.downloader
- numpy

#
# USING THE SCRIPTS
#

1. Configure your projects in 'projects.py' -- the file contains comments showing how to do this

2. Define your Twitter API keys and base data directory path in 'config.py'; the base directory refers to the
   ./data/ subdirectory in the Github repository as default which will work without changes unless you want
   to move the data output to another location

3. Run 'tweezo.py' without any arguments and follow the prompts - this is an interactive tool for orchestrating
   all other scripts which takes user input from prompts to orchestrate actions

   or

   Run 'twz.py' passing in command line arguments -- this is a script for orchestrating all other scripts which
   takes user input as arguments to orchestrate actions per the following:

   twz.py <action> <project or recipe>

   If running the 'compare', 'embeds', 'sentiment', 'wordcount' or 'tfidf' actions a third argument is provided
   to specify the date range for the analysis:

   twz.py <action> <project> <YYYY or YYYY-MM>

   If running the 'compare' action add a second project for comparison:

   twz.py <action> <project> <YYYY or YYYY-MM> <project2>

   If running the 'embeds' action add a threshold for analysis:

   twz.py <action> <project> <YYYY or YYYY-MM> <threshold>

   If running the 'sentiment' action add a choice of 'valence', 'arousal' or 'dominance' metric for the
   timeseries graph:

   twz.py <action> <project> <YYYY or YYYY-MM> <metric>

You should not invoke the other scripts directly. They won't work and need to be invoked via either 'tweezo.py'
or 'twz.py'.

#
# BACKGROUND SOURCES
#

The approach taken in these scripts has been inspired by several sources and, in some cases, liberally borrows
code snippets as the basis of the approach taken in these scripts' code. Key sources include:

1. Yanofsky's tweetdump.py (https://gist.github.com/yanofsky/5436496) provides the approach taken to scraping
   an initial set of tweets from a user timeline and then performing subsequent scrapes to get new tweets to
   add to a corpora for the user's timeline.

2. As these scripts were developed as part lab work in the Central European Univerity Digital Tools course for
   BA students in the 2020-21 academic year, many code samples and approaches presented in the course and lab
   materials are used in these scripts.

3. Earth Lab's online courses for performing social media analysis with Python
   (https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/
   social-media-text-mining-python/) were a critical learning tool for learning approaches to Twitter analysis
   and informed many of the approached in these scripts.

4. Mukesh Chaudry's article on using the SciKit-Learn TF-IDF Vectorizer
   (https://medium.com/@cmukesh8688/tf-idf-vectorizer-scikit-learn-dbc0244a911a) was very useful at gaining an
   understanding of how to use this library to perform TF-IDF analysis in these scripts.

5. Another useful resource in understanding TF-IDF in practice was Toward Data Science's article on TF-IDF in
   Python (https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-
   dataset-796d339a4089).

Other sources provided useful conceptual understanding:

1. DW Zhou's discussion of sentiment analysis scoring (https://github.com/dwzhou/SentimentAnalysis)

2. GeeksforGeek's discussion of time series plots with rolling averages in Python
   (https://www.geeksforgeeks.org/how-to-make-a-time-series-plot-with-rolling-average-in-python/)

Finally, these scripts depend on the following sentiment lexicon data source which has been replicated in CSV files
included with the scripts (full details in lexicon/readme.txt):

1. warriner.csv: sentiment lexicon file the research of Warriner, A. B., Kuperman, V., & Brysbaert, M.
              (2013). Norms of valence, arousal, and dominance for 13,915 English lemmas. Behavior
              research methods, 45(4), 1191-1207. (http://crr.ugent.be/archives/1003)
