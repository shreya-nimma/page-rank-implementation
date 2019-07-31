import networkx as nx
from operator import add
import heapq
import random
import time

def page_rank_large_dataset():
	'''
	This method implements PageRank on a dataset of ~800k nodes and ~5 billion edges. 
	This implementation uses custom defined methods to implement the sparse matrix representation
	required to hold data for this dataset. It is slower in comparison to the implementation that
	uses scipy library functions. 

	It does not solve spider traps or dead ends due to the transition matrix 
	becoming dense in both cases and computation time becoming infeasible.

	An epsilon value of 1.6e-2 has been used to determine convergence of the
	PageRank vector. The maximum number of iterations allowed is 1000.

	Its outputs are the final PageRank vector which is written to page_rank_vector_results/results_large.txt
	and a visualization of its subgraph, which is written in GEXF format to gexf_files/massive.gexf.
	
	'''
	program_start = time.time()
	max_iterations = 1000
	# Holds the largest node ID.
	largest_node_value = 0
	links = {}

	def matrix_mul(page_rank_vector):
		'''
		This method implements matrix multiplication between the vector passed as input
		and the sparse transition matrix that is represented by a dictionary of dictionaries.

		Output: The product of matrix multiplication.
		'''
		new_page_rank_vector = [0] * len(page_rank_vector)
		for row in links.keys():
			s = 0
			for col in links[row].keys():
				s += links[row][col] * page_rank_vector[col]
			new_page_rank_vector[row] = s
		return new_page_rank_vector

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
				elif (point[1] > largest_node_value):
					largest_node_value = point[1]
				coordinates.append(point)

	print ("Coordinates: %d" % len(coordinates))
	print ("Nodes: %d " % largest_node_value)

	# Storing the sum of all the links in each col to divide by later.
	no_of_nodes = largest_node_value + 1
	col_sum = [0] * no_of_nodes

	# Storing the sparse matrix as a linked list. Outer dictionary keys: rows. Nested dictionary keys: columns.
	for link in coordinates:
		if link[1] not in links.keys():
			links[link[1]] = {}
		if link[0] not in links[link[1]].keys():
			links[link[1]][link[0]] = 0.0
		links[link[1]][link[0]] += 1.0
		if links[link[1]][link[0]] > 1.0:
			print ("Duplicate edge found.")
		col_sum[link[0]] += 1.0

	# Making transition matrix stochastic
	for i in links.keys():
		for j in links[i].keys():
			links[i][j] /= col_sum[j]
	print("Sparse, stochastic transition matrix formed")

	# Forming initial PageRank vector
	page_rank_vector = [1/no_of_nodes] * no_of_nodes
	print ("Formed initial PageRank vector")

	# Power Iteration
	print ("Power iterating ... Max iterations = %d ...using epsilon value of 1.6e-2." % max_iterations)
	power_iteration_start = time.time()
	for i in range(max_iterations):
		new_page_rank_vector = matrix_mul(page_rank_vector)
		diff = 0
		for i in range(len(page_rank_vector)):
			diff += abs(new_page_rank_vector[i] - page_rank_vector[i])
		print ("Iteration done. Difference = %f"  % diff)
		page_rank_vector = new_page_rank_vector
		if diff < 0.016:
			print ("Page rank vector reached convergence.")
			break
	power_iteration_time = time.time() - power_iteration_start
	print ("Power iteration finished")

	# Storing results
	with open("page_rank_vector_results/results_large.txt", "w") as f:
		for i in range(len(page_rank_vector)):
			print (page_rank_vector[i], file = f)
	print ("You can view final PageRank vector in results_large.txt")

	# Creating a visual representation in GEXF format
	G = nx.DiGraph()

	# Extracting a subgraph for visualization
	selected_nodes = 0
	selected_nodes_ids = []
	for point in coordinates:
		if selected_nodes < 3000:
			if point[0] not in selected_nodes_ids:
				selected_nodes_ids.append(point[0])
				G.add_node(point[0], size=page_rank_vector[point[0]])
				selected_nodes += 1
			if point[1] not in selected_nodes_ids:
				selected_nodes_ids.append(point[1])
				G.add_node(point[0], size=page_rank_vector[point[1]])
				selected_nodes += 1
			G.add_edge(point[0], point[1])

	# Writing the graph
	print ("Writing a subgraph...")
	nx.write_gexf(G, "gexf_files/massive.gexf")

	print ("Open gexf_files/massive.gexf in Gephi to view the visual representation of the graph.")

	program_time = time.time() - program_start
	print ("Total program time %f secs. Power iteration time %f secs." % (program_time, power_iteration_time))