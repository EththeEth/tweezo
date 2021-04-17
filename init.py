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
#   Script: init.py
#
#   Initialise a new project if not already set up
#
#   This includes:
#
#   1. Creating necessary directories
#
#   2. Performing initial scrape
#
#   You need to run this script at least once after creating
#   a new project definition in 'projects.py'
#
#   It is safe to run this script against existing projects
#   as it will do nothing if all directories exist and
#   initial tweet scraping data exists
#
################################################################
#
#   The approach taken in this script to scrape an initial set
#   of tweets from a user timeline (and some parts of the
#   code) are based off Yanofsky's tweetdumper.py:
#
#   https://gist.github.com/yanofsky/5436496
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
# Define paths for a new project
#

projpath = config.basepath + project['key']
rawpath = config.basepath + project['key'] + '/raw/'
cleanpath = config.basepath + project['key'] + '/cleaned/'
analysispath = config.basepath + project['key'] + '/analysis/'

#
# Fetch Twitter user handle for project
#

screen_name = project['query']

#
# Check if directories are missing and if they are, create them
#

# Project directory
print('Checking for ' + projpath)
if (os.path.exists(projpath) == False or os.path.isdir(projpath) == False):

    # Create the project directory

    print('Creating ' + projpath)
    os.mkdir(projpath)

# Raw directory
print('Checking for ' + rawpath)
if (os.path.exists(rawpath) == False or os.path.isdir(rawpath) == False):

    # Create the raw directory

    print('Creating ' + rawpath)
    os.mkdir(rawpath)

# Clean directory
print('Checking for ' + cleanpath)
if (os.path.exists(cleanpath) == False or os.path.isdir(cleanpath) == False):

    # Create the clean directory

    print('Creating ' + cleanpath)
    os.mkdir(cleanpath)

# Analysis directory
print('Checking for ' + analysispath)
if (os.path.exists(analysispath) == False or os.path.isdir(analysispath) == False):

    # Create the analysis directory

    print('Creating ' + analysispath)
    os.mkdir(analysispath)

#
# Check if we need to scrape initial tweets by grabbing file list from raw and seeing
# if the directory is empty or not
#

print('Checking if we need to perform an initial tweet scrape')

filelist = os.listdir(rawpath) # Get all files in target directory

if len(filelist) == 0:

    #
    # Function to fetch the most recent max 3240 tweets from a user's
    # timeline
    #

    def get_all_tweets(screen_name):

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

        print(f"getting tweets first 200 tweets")

        #
        # Make initial request for most recent tweet since last
        # download (200 is the maximum allowed count)
        #

        new_tweets = api.user_timeline(screen_name=screen_name, count=200)

        #
        # Add these tweets to the list
        #

        alltweets.extend(new_tweets)

        #
        # Get the ID of the oldest tweet in the list (and the list is
        # reverse chronological) then subtract 1 -- so we start fetching
        # before the oldest tweet
        #

        oldest = alltweets[-1].id - 1

        #
        # Keep the user updated
        #

        print(f"...{len(alltweets)} tweets downloaded so far")

        #
        # Keep fetching tweets if the last fetch contained tweets and
        # keep going until we come up empty
        #

        while len(new_tweets) > 0:

            #
            # Keep the user informed
            #

            print(f"getting tweets before {oldest}")

            #
            # Fetch next batch of tweets using max_id to limit to tweets before
            # the ones we already have
            #

            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

            #
            # Add these tweets to the list
            #

            alltweets.extend(new_tweets)

            #
            # Get the ID of the oldest tweet in the list (and the list is
            # reverse chronological) then subtract 1 -- so we start fetching
            # before the oldest tweet
            #

            oldest = alltweets[-1].id - 1

            #
            # Keep the user updated
            #

            print(f"...{len(alltweets)} tweets downloaded so far")

        #
        # Get ID of the newest tweet to use for the CSV file name
        #

        newest = alltweets[0].id

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

        filename = rawpath + str(newest) + ".csv"  # Filename is <TweetID>.csv, where TweetID is last tweet pulled

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

    #
    # We have not files so we need to scrape so tell the user
    #

    print('Performing initial tweet scrape')
    print(project)
    print(screen_name)

    #
    # Scrape the first set of tweets
    #

    get_all_tweets(screen_name)
