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
#   Script: embeds.py
#
#   Perform word embedding analysis on tweets and produce a
#   word network graph.
#
#   Make sure 'dedup.py' has been run on your project's tweet
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
import networkx as nx
import itertools as it
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
import nltk
nltk.download('stopwords')
from gensim.models import Word2Vec
import gensim.downloader as api
import config

#
# Utility function to plot network graph and
# save the resulting graph in a specified file
#
# Function takes six arguments:
#
# net: the networkx object of the network to graph
#
# thres: threshold value to limit the graph to only
# nodes with similarity values greater than the threshold
#
# node_options: options to pass to draw_network_nodes
#
# filename: filename and path to save the graph
#
# label_options: options to pass to draw_network_labels
# (defaults to 'None')
#
# seed: seed value for the spring layout (default to '1')
#

def plot_network(net, thres, node_options, filename, label_options=None, seed=1):

    #
    # Initalise lists to hold list of edges, weights and widths
    #

    edgelist = []
    weights = []
    widths = []

    #
    # Loop through links and weights and add eddges and weights
    # to the lists above if their weight exceeeds the threshold
    #

    for i, j, w in net.edges.data('weight'):

        #
        # Check if we exceed the threshold
        #

        if w > thres:

            #
            # If we exceed the threshold, add to edgelist and weights
            #

            edgelist.append((i, j))
            weights.append(w)

    #
    # Normalise weights based on max/min values in weights list
    #
    # We need to loop through links and weights again to do this
    #

    for i, j, w in net.edges.data('weight'):

        #
        # Check if we exceed the threshold
        #

        if w > thres:

            #
            # If we exceed the threshold, normalise
            #

            widths.append(1 + (w - min(weights)) / (max(weights) - min(weights)))

    #
    # Initialise figure in matplotlib -- set the size of image driven by number
    # of edges with a simplistic formula with an upper limit on pixels
    #

    fig_width = int(len(edgelist) / 5)
    fig_height = int(fig_width * 0.8)

    if (fig_width > 78):
        fig_width = 78
        fig_height = 60

    if (fig_width < 26):
        fig_width = 26
        fig_height = 20

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    #
    # Calculate node positions according to spring layout
    #

    node_pos = nx.spring_layout(net, seed=seed)

    #
    # Draw nodes with specified options
    #

    node_draw = nx.draw_networkx_nodes(net, node_pos, **node_options)

    #
    # Draw node labels with specified options
    #

    #
    # Draw labels if 'label_options' exists
    #

    if label_options:
        label_draw = nx.draw_networkx_labels(net, node_pos, **label_options)

    #
    # Set edge drawing options
    #

    edge_options = {
        'edgelist': edgelist,
        'width': widths,
        'edge_color': weights,
        'edge_cmap': cm.get_cmap('winter_r'),
        'edge_vmin': min(weights),
        'edge_vmax': max(weights),
    }

    #
    # Draw edges with specified options
    #

    edge_draw = nx.draw_networkx_edges(net, node_pos, **edge_options)

    #
    # Draw colorbar with weight values
    #

    cbar = plt.colorbar(edge_draw, shrink=0.5, aspect=10)
    cbar.set_label('word2vec similarity')

    #
    # Save the graph to the specified file
    #

    plt.savefig(filename)

#
# Define paths for analysis files.
#
# The 'analysis' subdirectory stores various data files generated
# in the analysis process including generated graphs etc
#

analysispath = config.basepath + project['key'] + '/analysis/'

#
# Create list to hold list of tweet words
#

content = []

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
            # Grab the lemmas as a string of text (which is what comes from the CSV
            # and strip out the leading [' and trailing '] so we can split in the next step
            #
            # In the CSV the field looked like:
            #
            # ['word1','word2', ... ,'wordX']
            #
            # So, the [-2:2] syntax gives us:
            #
            # word1','word2', ... ,'wordX
            #

            lemmas = row['lemmas'][2:-2]

            #
            # Split the lemmas string into a list of words using the following
            # string to split:
            #
            # ','
            #
            # Add the words to the words list
            #

            content.append(lemmas.split('\', \''))

#
# Get the Google News word2vec model to use on our Twitter data set
#

wordvectors = api.load( 'word2vec-google-news-300' )

#
# Flatten tweet list with itertools (and transform to set to remove word duplicates)
#

content_flat = set( it.chain( *content ) )

#
# Create object to hold similarities data
#

similarities = {}  # initialise dict of word similarities

#
# Loop through all unique 2-word combinations and save similarities data
#
# Make sure we only include tuples with terms that are in the Google model
#

for word_tuple in list(it.combinations(content_flat, 2)):

    #
    # Check if both words are in the Google model
    #

    if word_tuple[0] in wordvectors and word_tuple[1] in wordvectors:
        similarities[word_tuple] = wordvectors.similarity(word_tuple[0], word_tuple[1])

#
# Save similarities data to a .csv file as well as
# .csv files of most and least similar 25 tuples
#

similarities_df = pd.DataFrame(sorted(similarities.items(), key=lambda item: item[1], reverse=True))
similarities_df.to_csv(analysispath + 'similarities_' + year + '.csv')
similarities_df.head(25).to_csv(analysispath + 'most_similar_' + year + '.csv')
similarities_df.tail(25).to_csv(analysispath + 'least_similar_' + year + '.csv')

#
# Slow script, so keep the user updated
#

print('Generating word network object')


#
# Initialise a word network object
#

net = nx.Graph()

#
# Loop through word pairs and their similarity values
#

for word_pair, sim_val in similarities.items():
    net.add_edge(word_pair[0], word_pair[1], weight=sim_val)


degrees = dict(net.degree)

#
# Set node drawing options
#

node_options = {
    'node_size' : 50
}

#
# Set label drawing options
#

label_options = {
    'font_size' : 8,
    'verticalalignment' : 'bottom'
}

#
# Slow script, so keep the user updated
#

print('Plotting network graphs')

#
# Plot network
#

plot_network(net, thres=thres, node_options=node_options, filename=analysispath + 'embeds_' + str(thres) + '_' + year + '.png', label_options=label_options)
plot_network(net, thres=thres, node_options=node_options, filename=analysispath + 'embeds_nolabels_' + str(thres) + '_' + year + '.png', label_options=None)
