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
#   Script: twz.py
#
#   Orchestration script to allow user to control which action
#   to take for which project(s) via command line invocation
#
#   The script takes a simple series of arguments in a fixed
#   order:
#
#   1. Action to perform
#
#   2. Project for processing or recipe for processing
#
#   The following only apply when not using the 'recipe'
#   action:
#
#   3. YYYY or YYYY-MM to limit the analysis range (for
#      'compare', 'embeds', 'sentiment', 'wordcount' and
#      'tfidf' actions only)
#
#   4. Second project for comparison (for 'compare' action
#      only
#
#   5. Threshold for network graph (for 'embeds' action only)
#
#   6. 'valence', 'arousal' or 'dominance' to specify the
#      timeseres to plot (for 'sentiment' action only)
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

import sys
import config

#
# Get the action (first argument)
#

my_action = sys.argv[1]

#
# If the action is 'recipe' then process the recipe otherwise
# process action against project specified
#

if (my_action == 'recipe'):

    #
    # Get the recipe
    #

    recipe = config.recipes[sys.argv[2]]

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

    if ('threshold' in recipe):
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
    # Get the project (second argument)
    #

    my_project = sys.argv[2]

    #
    # Define project object for dependent scripts
    #

    project = {}
    project['key'] = my_project
    project['query'] = config.projects[my_project]['query']
    project['stopwords'] = config.projects[my_project]['stopwords']

    #
    # If the action is one of the following get the year/month from the
    # third argument:
    #
    # wordcount
    # tfidf
    # sentiment
    # compare
    # embeds
    #

    if (my_action in ['wordcount','tfidf','sentiment','compare','embeds']):
        year = sys.argv[3]

    #
    # If the action is "compare" we need a project to compare to (fourth
    # argument):
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
        # Get user's choice of comparison project and store in shift list
        #

        shift.append(sys.argv[4])

    #
    # If the action is "embeds", get the threshold
    #
    # Because the argument is a string we convert to a number with 'float'
    #

    if (my_action in ['embeds']):
        thres = float(sys.argv[4])

    #
    # If the action is "sentiment", get the metric for the timeseries
    # graph (fourth argument):
    #

    if (my_action in ['sentiment']):
        metric = sys.argv[4]

    #
    # Execute action on project
    #

    print()
    print('Perform ' + my_action + ' on ' + my_project)

    #
    # Call target script
    #

    exec(open(my_action + ".py").read())

