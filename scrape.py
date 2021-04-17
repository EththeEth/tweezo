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
#   Script: scrape.py
#
#   Retrieve all tweets for a specified Twitter user since
#   the last tweet scraped
#
################################################################
#
#   The approach taken in this script (and some parts of the
#   code) are based off Yanofsky's tweetdumper.py:
#
#   https://gist.github.com/yanofsky/5436496
#
#   This approach is modified here to retrieve all tweets from
#   a specific user since the last retrieval and store as
#   .csv files
#
#   This code is a free and unencumbered software project
#   released into the public domain.
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

import tweepy
import csv
import os
import config

#
# Fetch Twitter keys from config
#

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_key = config.access_key
access_secret = config.access_secret

#
# Define path for raw CSV files
#
# The 'raw' subdirectory stores raw scraped tweets in CSV files
#

rawpath = config.basepath + project['key'] + '/raw/'

#
# Fetch Twitter user handle for project
#

screen_name = project['query']

#
# Get last tweet ID from file names; files are stored as <TweetID>.csv
#

filelist = os.listdir(rawpath) # Get all files in target directory
filelist.sort() # Sort files alphanumerically

#
# Determine the last tweet ID by checking the file name of the last
# available file in the list (since the files are sorted by name)
# and stripping off the '.csv' extension
#
# Breaking this down:
#
# filelist[-1] uses a negative list index to fetch the last element in
# the list
#
# split('.')[0] splits the file name into two pieces using the dot as
# separator and returns the first part (at index 0) which will be the
# tweet ID of the last tweet in that CSV file
#
# If the directory is empty, this doesn't happen and 'lasttweet' will
# be an empty string
#

lasttweet = ''

if len(filelist) > 0:
    lasttweet = filelist[-1].split('.')[0]

#
# If 'lasttweet' is not zero then we can fetch tweets
# and it not it means the project isn't initialised
# so we can't fetch tweets
#

if lasttweet != '':

    #
    # Twitter Authorisation and Tweepy initialisation
    #

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #
    # Initialise a list to hold all the tweepy Tweets
    #

    alltweets = []

    #
    # Output some info for the user to keep them posted on progress
    #
    print(f"getting tweets after {lasttweet}")

    #
    # Make initial request for most recent tweet since last
    # download (200 is the maximum allowed count)
    #

    new_tweets = api.user_timeline(screen_name=screen_name, count=200, since_id=lasttweet)

    #
    # Only process and fetch more tweets if there are any available
    #
    # We determine this by checking the length of the list of tweets we just
    # fetched
    #

    if len(new_tweets) > 0:

        #
        # Save most recent tweets by using extend() to add them to the
        # 'alltweets' list we created earlier to hold all the tweets
        #

        alltweets.extend(new_tweets)

        #
        # Save the ID of the newest tweet which will be the ID of the
        # first tweet in the list because the way tweets are sorted
        # (reverse chronological)

        newest = alltweets[0].id

        #
        # Output some info for the user to keep them posted on progress
        #
        print(f"...{len(alltweets)} tweets downloaded so far")

        #
        # Keep grabbing tweets until there are no tweets left to grab
        #
        # We do this with the same technique as above, but using a
        # while loop to keep going until our condition is true
        # (i.e. that we get no tweets back to our last request)

        while len(new_tweets) > 0:

            #
            # Output some info for the user to keep them posted on progress
            #
            print(f"getting tweets after {newest}")

            #
            # Fetch the next batch of tweets using the since_id parameter
            # to prevent duplication
            #

            new_tweets = api.user_timeline(screen_name=screen_name, count=200, since_id=newest)

            #
            # Save most recent tweets in the alltweets list
            #

            alltweets.extend(new_tweets)

            #
            # Update the ID of the newest tweet
            #

            newest = alltweets[0].id

            #
            # Output some info for the user to keep them posted on progress
            #
            print(f"...{len(alltweets)} tweets downloaded so far")

        #
        # Transform the tweepy tweets into a 2D array that will populate the .csv
        #

        outtweets = [[tweet.id_str, tweet.text, tweet.favorite_count, tweet.retweet_count, tweet.created_at,
                      tweet.source, tweet.in_reply_to_status_id, tweet.in_reply_to_screen_name]
                     for tweet in alltweets]

        #
        # Determine the file name for the csv containing the newly scraped
        # tweets where the file name uses the last tweet's ID number
        # (in 'newest')
        #

        filename = rawpath + str(newest) + ".csv" # Filename is <TweetID>.csv, where TweetID is last tweet pulled

        #
        # Open the file for writing and use the csv module to write out
        # the contents of 'outtweets' into rows in a CSV
        #

        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['tweet_id', 'text', 'favorite_count', 'retweet_count', 'created_at', 'source',
            'in_reply_to_status_id', 'in_reply_to_screen_name'])
            writer.writerows(outtweets)

        pass
