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
#   Script: recipes-sample.py
#
#   Purpose: User-defined list of recipe definitions to define
#   pre-packaged sets of actions on a pre-specified project.
#
#   USING THIS FILE:
#
#   This is a sample file. Copy it to recipes.py and edit it
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
# Create 'recipes' object to hold a list of recipes
#
# DO NOT change this object name
#

recipes = {} # Do not edit/remove -- this is not configurable

#
# Define list of recipes -- each recipe is defined as follows:
#
# Set up an empty object for the recipe and specify the name
# of the recipe as the key (this name is used to refer to the
# recipe when invoking):
#
# recipes['<key>'] = {}
#
# Specify the project the recipe applies to:
#
# recipes['<key>']['project'] = <project>
#
# Specify the list of actions to perform in the recipe in the
# order desired:
#
# recipes['<key>']['actions'] = ['<action1>','<action2>',...]
#
# If using the 'compare', 'embeds, 'sentiment', 'wordcount'
# or 'tfidf' actions, specify the dates to analyse as YYYY
# or YYYY-MM:
#
# recipes['<key>']['dates'] = <YYYY or YYYY-MM>
#
# If using the 'compare' action, specify the second project
# for comparison:
#
# recipes['<key>']['project2'] = <project2>
#
# If using the 'embeds' action, specify the threshold for the
# network graph:
#
# recipes['<key>']['threshold'] = <threshold>
#
# If using the 'sentiment' action, specify the metric as
# 'valence', 'arousal' or 'dominance':
#
# recipes['<key>']['metric'] = <metric>

# Sample Recipe configure to scrape a sample project's timeline,
# clean and dedup
recipes['sample'] = {}
recipes['sample']['project'] = 'sample_project'
recipes['sample']['actions'] = ['scrape','clean','dedup']

# Sample Recipe configure to scrape a sample project's timeline,
# clean and dedup and then perform wordcount
recipes['sample2'] = {}
recipes['sample2']['project'] = 'sample_project'
recipes['sample2']['actions'] = ['scrape','clean','dedup','wordcount']
recipes['sample2']['dates'] = '2021-04'

# Sample Recipe configure to scrape a sample project's timeline,
# clean and dedup and then perform embeds and sentiment
recipes['sample3'] = {}
recipes['sample3']['project'] = 'sample_project'
recipes['sample3']['actions'] = ['scrape','clean','dedup','embeds','sentiment']
recipes['sample3']['dates'] = '2021-04'
recipes['sample3']['threshold'] = 0.4
recipes['sample3']['metric'] = 'dominance'

# Repeat project defintions as needed
#recipes['sample4'] = {}
#recipes['sample4']['project'] = 'sample_project'
#recipes['sample4']['actions'] = ['scrape','clean','dedup']
#etc.