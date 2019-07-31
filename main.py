import sys
from py.enhancement import page_rank_large_dataset
from py.regular import page_rank_regular_dataset
from py.scipy_enhancement import page_rank_large_dataset_scipy

def main():
	'''
	Main function that allows the user to choose which implementation
	of PageRank to run.

	'''
	large = input("Enter 'L' for large dataset, or 'R' for regular dataset.\n")

	if (large == 'L' or large == 'l'):
		fast = input("Enter 'F' for fast computation (using scipy), or 'S' for slower computation (manual implementation).\n")
		print ("--------------------")
		if (fast == 'S' or fast == 's'):
			page_rank_large_dataset()
		else:
			page_rank_large_dataset_scipy()
	else:
		print ("--------------------")
		page_rank_regular_dataset()

if __name__ == "__main__":
	main()
	




