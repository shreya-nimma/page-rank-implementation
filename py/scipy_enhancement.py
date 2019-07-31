from scipy.sparse import csc_matrix 	# For the sparse web transition matrix
from sklearn.preprocessing import normalize
import numpy as np 						# For the eigenvector matrix
import networkx as nx
import time

def page_rank_large_dataset_scipy():
	'''
	This method implements PageRank on a dataset of ~800k nodes and ~5 billion edges. 
	This implementation uses scipy library functions to implement sparse matrix
	representation for performance benefits. It does not solve spider traps or dead 
	ends due to the transition matrix becoming dense in both cases and computation
	time becoming infeasible.

	An epsilon value of 1.6e-2 has been used to determine convergence of the
	PageRank vector. The maximum number of iterations allowed is 1000.

	Its outputs are the final PageRank vector which is written to page_rank_vector_results/scipy_massive_results.txt
	and a visualization of its subgraph, which is written in GEXF format to gexf_files/scipy_massive.gexf.

	'''
	program_start = time.time()
	# Holds the largest node ID.
	largest_node_value = 0

	max_iterations = 1000

	# Reading in the co-ordinates.
	coordinates = []

	# Skips the first four lines of the document
	skiplines = 4
	with open("datasets\web-Google.txt", "r") as f:
		for line in f:
			if(skiplines != 0):
				skiplines -= 1
			else:
				point = []
				point.append(int(line.split()[0]))
				point.append(int(line.split()[1]))
				if (point[0] > largest_node_value):
					largest_node_value = point[0]
				if (point[1] > largest_node_value):
					largest_node_value = point[1]
				coordinates.append(point)

	print ("Coordinates: %d" % len(coordinates))
	print ("Nodes: %d " % largest_node_value)

	# Creating lists to feed into the sparse matrix constructor
	no_of_points = len(coordinates)
	no_of_nodes = largest_node_value + 1
	values = [1.0] * no_of_points
	rows = [point[1] for point in coordinates]
	cols = [point[0] for point in coordinates]

	# Creating a sparse matrix
	transition_matrix = csc_matrix((values, (rows, cols)), shape=(no_of_nodes, no_of_nodes))
	print ("Transition matrix created.")

	# Making the sparse matrix stochastic
	transition_matrix = normalize(transition_matrix, norm='l1', axis=0)
	print ("Transition matrix made stochastic.")

	# Creating initial page rank vector
	page_rank_vector = [1/no_of_nodes] * no_of_nodes

	print ("Power iterating ... Max iterations = %d ...using epsilon value of 1.6e-2." % max_iterations)
	power_iteration_start = time.time()
	for i in range(max_iterations):
		new_page_rank_vector = transition_matrix.dot(page_rank_vector)

		difference = np.subtract(new_page_rank_vector, page_rank_vector)
		difference = np.absolute(difference)
		s = difference.sum()
		print ("Difference: %f " % s)
		page_rank_vector = new_page_rank_vector
		if s < 0.016:
			print ("Page rank vector has reached convergence after %i iterations." % (i+1))
			break
	power_iteration_time = time.time() - power_iteration_start
	print ("Power iteration done.")

	# Writing pagerank output to a file
	print ("You can view the final PageRank vector in page_rank_vector_results/scipy_massive_results.txt")
	np.savetxt('page_rank_vector_results/scipy_massive_results.txt', page_rank_vector)
	p = page_rank_vector.sum()
	page_rank_vector = page_rank_vector.tolist()

	# Creating a visual representation in GEXF format
	print ("Writing a subgraph...")
	G = nx.DiGraph()

	# Extracting a subgraph for visualization
	selected_nodes = 0
	selected_nodes_ids = []
	for point in coordinates:
		if selected_nodes < 3000:
			if point[0] not in selected_nodes_ids:
				selected_nodes_ids.append(point[0])
				G.add_node(point[0], size=page_rank_vector[point[0]], label=point[0])
				selected_nodes += 1
			if point[1] not in selected_nodes_ids:
				selected_nodes_ids.append(point[1])
				G.add_node(point[1], size=page_rank_vector[point[1]])
				selected_nodes += 1
			G.add_edge(point[0], point[1])
			
	# Writing the graph
	nx.write_gexf(G, "gexf_files/scipy_massive.gexf")
	print ("Subgraph has been written. You can open the graph file gexf_files/scipy_massive.gexf to view the graph.")

	program_time = time.time() - program_start
	print ("Total program time %f secs. Power iteration time %f secs." % (program_time, power_iteration_time))
	# print ("%f percent of PageRank retained." % (p*100))