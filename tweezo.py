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
#   Script: tweezo.py
#
#   Orchestration script to allow user to control which action
#   to take for which project(s) with interactive prompts
#
#   This should be the only script you need to directly run and
#   the other scripts will not run unless invoked from this
#   script as this script sets up some key variables the other
#   scraping and processing scripts depend on
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


import config

#
# Does the user want to user a recipe?
#

print()
use_recipe = input('Do you want to use a recipe (Y or N)? ')
print()

#
# If using a recipe, let the user choose a recipe and set up variables
# otherwise prompt user for project, action, etc
#

if (use_recipe == 'Y'):

    #
    # Print list of defined recipes
    #

    print('Choose a recipe:')
    print()

    for recipe in config.recipes:
        print(recipe)

    print()

    #
    # Get user's choice of recipe
    #

    my_recipe = input('Which recipe do you want to use? ')
    recipe = config.recipes[my_recipe]

    print()

    #
    # Get the project
    #

    my_project = recipe['project']

    #
    # Define project object for dependent scripts
    #

    project = {}
    project['key'] = my_project
    project['query'] = config.projects[my_project]['query']
    project['stopwords'] = config.projects[my_project]['stopwords']

    #
    # If we have a year, get it
    #

    if ('dates' in recipe):
        year = recipe['dates']

    #
    # If we have a threshold, get it
    #

    if ('threshold'in recipe):
        thres = recipe['threshold']

    #
    # If we have a metric, get it
    #

    if ('metric' in recipe):
        metric = recipe['metric']

    #
    # If we have a comparator set it up
    #

    if ('project2' in recipe):

        #
        # Define shift object needed for comparison
        #
        # This list will have two elements:
        #
        # The key for the first project to compare
        # The key for the second project to compare
        #

        shift = []
        shift.append(project['key'])

        #
        # Get user's choice of comparison project and store in shift list
        #

        shift.append(recipe['project2'])

    #
    # Loop through list of actions and perform them
    #

    for my_action in recipe['actions']:

        #
        # Execute action on project
        #

        print()
        print('Perform ' + my_action + ' on ' + my_project)

        #
        # Call target script
        #

        exec(open(my_action + ".py").read())

else:

    #
    # Print list of defined projects
    #

    print('Choose a project:')
    print()

    for project in config.projects:
        print(project)

    print()

    #
    # Get user's choice of project
    #

    my_project = input('Which project do you want to use? ')

    print()

    #
    # Print list of available actions
    #

    print('Choose an action:')
    print()

    print('"init": Initialise new project and download tweets')
    print('"scrape": Scrape new tweets')
    print('"clean": Preprocess scraped tweets')
    print('"dedup": Deduplicate content in scraped tweets')
    print('"wordcount": Wordcount analysis')
    print('"tfidf": TF-IDF analysis')
    print('"sentiment": Sentiment analysis')
    print('"compare": Perform comparison analysis on tweets in two projects')
    print('"embeds": Perform word embedding analysis')

    print()

    #
    # Get user's choice of actions
    #

    my_action = input('Which action do you want to perform? ')

    print()

    #
    # Define project object for dependent scripts
    #

    project = {}
    project['key'] = my_project
    project['query'] = config.projects[my_project]['query']
    project['stopwords'] = config.projects[my_project]['stopwords']

    #
    # If the action is "compare" we need a project to compare to:
    #
    if (my_action in ['compare']):

        #
        # Define shift object needed for comparison
        #
        # This list will have two elements:
        #
        # The key for the first project to compare
        # The key for the second project to compare
        #

        shift = []
        shift.append(project['key'])

        #
        # We need a second project to compare with
        #
        # Print list of defined projects excluding the
        # project already selected above
        #

        print()

        print('Choose a project to compare ' + shift[0] + ' with:')
        print()

        for project in config.projects:
            if shift[0] != project:
                print(project)

        print()

        #
        # Get user's choice of comparison project and store in shift list
        #

        shift.append(input('Which project do you want to use for comparison? '))

    #
    # If the action is one of the following then ask the user what year
    # (or year and month) of tweets they want to analyse -- to reduce
    # the size of the data being processed -- otherwise some of the
    # generated results are too dense to be useful:
    #
    # wordcount
    # tfidf
    # sentiment
    # compare
    # embeds
    #

    if (my_action in ['wordcount','tfidf','sentiment','compare','embeds']):
        print()
        year = input('What year (or year-month) do you want to analyse (YYYY or YYYY-MM)? ')

    #
    # If the action is "embeds", ask the user what threshold they want
    # to use for plotting the network graph -- too low and the graph
    # will never render
    #
    # Because 'input' returns a string we convert to a number with 'float'
    #

    if (my_action in ['embeds']):
        print()
        thres = float(input('What threshold do you want to use to restrict nodes when plotting the network graph? '))

    #
    # If the action is "sentiment", ask the user whether the timeseries
    # analysis for valence, arousal or dominance
    #

    if (my_action in ['sentiment']):
        print()
        print('In addition to rolling averages of valence, arousal and dominance, a timeseries analysis is');
        print('performed on one of the following:')
        print()

        print('"valence": the pleasantness of a stimulus')
        print('"arousal": the intensity of emotion provoked by a stimulus')
        print('"dominance": the degree of control exerted by a stimulus')

        print()

        metric = input('Which timeseries analysis do you wish to perform? ')

    #
    # Execute action on project
    #

    print()
    print('Perform ' + my_action + ' on ' + my_project)

    #
    # Call target script
    #

    exec(open(my_action + ".py").read())

