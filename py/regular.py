import numpy as np 
import networkx as nx
import time

def page_rank_regular_dataset():
	'''
	This method implements PageRank on a dataset of ~4k nodes and ~13k edges. 
	This implementation uses numpy library functions for matrix
	representation. 

	It solves spider traps using teleports and a beta value of 0.85. Dead ends 
	have a probability of 1 of teleporting to another node.

	An epsilon value of 1e-12 has been used to determine convergence of the
	PageRank vector. The maximum number of iterations allowed is 1000.

	Its outputs are the final PageRank vector which is written to page_rank_vector_results/results_regular.txt.txt
	and a visualization of its subgraph, which is written in GEXF format to gexf_files/regular.gexf.
	
	'''
	program_start = time.time()
	max_iterations = 1000
	beta = 0.85

	# Holds the largest node ID.
	largest_node_value = 0

	# Reading in the co-ordinates.
	coordinates = []

	# Skips the first four lines of the document
	skiplines = 4
	with open("datasets/small_dataset.txt", "r") as f:
		for line in f:
			if(line.split()[0] == "e"):
				point = []
				point.append(int(line.split()[2]))
				point.append(int(line.split()[1]))
				if (point[0] > largest_node_value):
					largest_node_value = point[0]
				elif (point[1] > largest_node_value):
					largest_node_value = point[1]
				coordinates.append(point)

	print ("Coordinates: %d" % len(coordinates))
	print ("Nodes: %d " % (largest_node_value+1))

	no_of_nodes = largest_node_value + 1

	# Initializing the transition matrix
	M = [0] * no_of_nodes
	for i in range(no_of_nodes):
		M[i] = [0] * no_of_nodes

	# Populating the transition matrix
	for link in coordinates:
		M[link[0]][link[1]] += 1

	# Converting it into a NumPy, stochastic matrix
	dead_ends = []
	M = np.matrix(M, dtype="float")
	sum_mat = M.sum(0)
	for i in range(no_of_nodes):
		if (sum_mat[0, i] != 0):
			M[:,i] /= float(sum_mat[0, i])
		else:
			dead_ends.append(i)

	# Adding taxation component to resolve dead ends and spider traps
	tax = (1-beta)*(1/no_of_nodes)
	for i in range(no_of_nodes):
		if i in dead_ends:
			M[:,i] += (1/no_of_nodes)
		else:
			M[:,i] *= beta
			M[:,i] += tax
	print ("Taxation component added to transition matrix to solve spider traps. Beta = %f " % beta)
	print ("There is 100% probability of teleportation at dead ends.")
	print ("Transition matrix complete.")

	# Creating an initial PageRank vector
	page_rank_vector = [1.0/no_of_nodes] * no_of_nodes
	page_rank_vector = np.matrix(page_rank_vector)
	page_rank_vector = page_rank_vector.transpose()
	print ("Page rank vector initialized.")

	# Power iterating
	print ("Power iterating ... Max iterations = %d ...using epsilon value of 1e-12." % max_iterations)
	power_iteration_start = time.time()
	for i in range(max_iterations):
		new_page_rank_vector = M.dot(page_rank_vector)
		difference = np.subtract(new_page_rank_vector, page_rank_vector)
		difference = np.absolute(difference)
		s = difference.sum()
		if s < 0.000000000001:
			print ("Page rank vector has reached convergence after %i iterations." % (i+1))
			page_rank_vector = new_page_rank_vector
			break
		# print (s)
		page_rank_vector = new_page_rank_vector
	power_iteration_time = time.time() - power_iteration_start

	print ("Percent of PageRank retained in vector: %f " % (page_rank_vector.sum()*100))

	# Printing results into file
	with open("page_rank_vector_results/results_regular.txt", "w") as F:
		for i in range(len(page_rank_vector)):
			print (page_rank_vector[i], file = F)

	print ("--------------------")
	print ("Open page_rank_vector_results/results_regular.txt to view final PageRank vector")

	# Creating a visual representation in GEXF format
	G = nx.DiGraph()

	# Adding nodes
	page_rank_vector = page_rank_vector.transpose()
	page_rank_vector = page_rank_vector.tolist()
	for i in range(len(page_rank_vector[0])):
		G.add_node(i, size = page_rank_vector[0][i]*100000)

	# Adding edges
	for point in coordinates:
		G.add_edge(point[1], point[0])

	# Writing the graph
	nx.write_gexf(G, "gexf_files/regular.gexf")

	print ("Open gexf_files/regular.gexf in Gephi to view the visual representation of the graph.")

	program_time = time.time() - program_start
	print ("Total program time %f secs. Power iteration time %f secs." % (program_time, power_iteration_time))






