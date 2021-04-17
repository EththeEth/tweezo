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
#   Script: config-sample.py
#
#   Purpose: Define key configuration for all other scripts
#   including Twitter API credentials, base path for storing all
#   output files, and import list of user-defined projecst from
#   projects.py
#
#   USING THIS FILE:
#
#   This is a sample file. Copy it to config.py and edit it
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
# Specify Twitter API credentials
#

consumer_key    = '<your key here>'
consumer_secret = '<your secret here>'
access_key      = '<your key here>'
access_secret   = '<your secret here>'

#
# Specify base path -- inside this directory there should be a
# subdirectory for each project defined which is named based on
# the project's key in the 'projects' object
#
# The path can be root relative or relative to the script's
# directory and should include the trailing slash or
# backslash as appropriate for the host OS
#
# The default location is './data/' which is a subdirectory
# of the directory containing these python scripts
#
# It can be changes as needed
#

basepath = './data/' # Include the trailing slash or backslash

#
# DO NOT EDIT AFTER THIS LINE
#

#
# Define a list of projects
#
# Do not edit or remove this section
#

import projects

projects = projects.projects
