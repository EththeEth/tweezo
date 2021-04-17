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
#   Script: projects-sample.py
#
#   Purpose: User-defined list of project settings for different
#   sets of tweets (by user timeline) to scrape and process.
#
#   USING THIS FILE:
#
#   This is a sample file. Copy it to projects.py and edit it
#   per below for your own use.
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
# Create 'projects' object to hold a list of projects
#
# DO NOT change this object name
#

projects = {} # Do not edit/remove -- this is not configurable

#
# Define list of projects -- each project is defined as follows:
#
# Set up an empty object for the project and specify the name
# of the project as the key (this name is used to refer to the
# project's subdirectory in the base path directory):
#
# projects['<key>'] = {}
#
# Specify the query string for the project -- which should be
# the twitter handle of the user whose tweets you want to
# scrape and process:
#
# projects['<key>']['query'] = '<User Handle>'
#
# Specify any custom stop words for the project:
#
# projects['<key>']['stopwords'] = ['<term1>','<term2>',...]
#
# If there are no custom stopwords, just use and empty list:
#
# projects['<key>']['stopwords'] = []
#
# These stopwords will be added to NLTK's English stopwords list
# when removing stopwords
#

# Sample Project configure to scrape Twitter's own account's timeline
projects['sample'] = {}
projects['sample']['query'] = 'Twitter'
projects['sample']['stopwords'] = ['twitter','tweet']

# Repeat project defintions as needed
#projects['sample2'] = {}
#projects['sample2']['query'] = 'Twitter'
#projects['sample2']['stopwords'] = ['twitter','tweet']
