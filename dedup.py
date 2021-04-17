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
#   Script: dedup.py
#
#   Takes the 'alltweets.csv' file from the 'analysis' directory
#   and deduplicates the tweet list based on tweet ID
#
#   Resulting file is 'alltweets_dedup.csv'
#
#   Typically this script should be run after cleaning newly-
#   scraped tweets with 'clean.py' as 'alltweets_dedup.csv'
#   is a dependency for the various analysis scripts which
#   use this CSV as the source for all tweet data in their
#   analysis
#
################################################################
#
#   The approach taken in this script (and some parts of the
#   code) are based on class lectures and notes from the
#   Digital Tools course for BA students in the 2020-21
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
import config

#
# Define paths for raw CSV files and cleansed CSV files.
#
# The 'analysis' subdirectory stores various data files generated
# in the analysis process including generated graphs etc
#

analysispath = config.basepath + project['key'] + '/analysis/'

#
# Open 'alltweets.csv' and read into a Pandas DataFrame
#

tweets = pd.read_csv(analysispath + 'alltweets.csv')

#
# Get a count of the tweets in the file with len()
#

count = len(tweets.index)

#
# Remove duplicates based on tweet ID
#

tweets.drop_duplicates(subset=['tweet_id'])

#
# Get a coount of the tweets after dropping duplicates
#

count_dedup = len(tweets.index)

#
# Output de-duplicated tweets in 'alltweets_dedup.csv'
# using Pandas to_csv() function
#

tweets.to_csv(analysispath + 'alltweets_dedup.csv')

#
# Keep the user updated by outputting the counts
# before and after removing duplicates
#

print('raw count: ' + str(count))
print('dedup count: ' + str(count_dedup))