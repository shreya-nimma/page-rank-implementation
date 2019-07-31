# PageRank Implementation

#### Language: Python v3.6.0

This project is an implementation of the Google PageRank algorithm. This code outputs the PageRank vector into a text file for viewing and writes a graph in GEXF format which can viewed using a suitable graph visualization tool. 

There are three implementations of PageRank within this program:

* For a regular-sized dataset (~4k nodes/~13k edges): Implementation of PageRank using numpy matrices. Incorporates a solution to dead-ends and spider-traps.
* For a large-sized dataset (~800k nodes/~5bil edges): Implementation of PageRank using own methods to handle sparse matrix representation and operations. 
* For a large-sized dataset (~800k nodes/~5bil edges): Implementation of PageRank using scipy library functions to handle sparse matrix representation. This implementation runs faster than the second.

## Prerequisities

You will need to install the following python libraries in order to run this code:

* numpy
* scipy
* networkx
* sklearn

You can install these through pip.

In addition, the Gephi tool is useful in viewing the graph represented in the GEXF file that is written by this program. You may download the tool from: https://gephi.org/

## Working

1. Run main.py
2. Select which implementation you wish to run. (Refer to introductory paragraph for information about the implementations.)
3. The final PageRank vector is written to the text file mentioned in the output of the program. The file can be found in the "page_rank_vector_results" folder.
4. The graph representing the network is written to a GEXF file mentioned in the output of the program. This file is located in the "gexf_files" folder.
5. You may view the resulting graph by opening the GEXF file using Gephi.
6. Saved images of graphs opened and adjusted in Gephi are present in the "visual_graph_results" folder.

## Acknowledgements

We sourced the dataset (Google Web Graph) for the PageRank implementation for large datasets from the SNAP Large Network Dataset Collection. https://snap.stanford.edu/data/web-Google.html

The dataset for the regular implementation was borrowed from Jon Kleinberg's "The Structure of Information Networks" Fall 2002 course. We used the "Pages linking to www.epa.gov" dataset linked from this wesbsite http://www.cs.cornell.edu/courses/cs685/2002fa/