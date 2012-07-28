#!/usr/bin/python -Wall

# ================================================================
# A die is rolled until the pip sum reaches 300.
# What is the probability that at least 80 rolls are necessary?
# John Kerl
# 2011-03-20
# ================================================================

import sys, random

# ----------------------------------------------------------------
def main():
	#print_trajectories()
	create_histogram_data()

# ----------------------------------------------------------------
def print_trajectories():
	sum_to_reach = 300
	num_experiments = 20
	if len(sys.argv) == 2:
		num_experiments = int(sys.argv[1])

	sums = [0] * num_experiments

	while True:

		# Print
		for i in range(0, num_experiments):
			print sums[i],
		print

		# Check for done
		all_done = True
		for i in range(0, num_experiments):
			if sums[i] < sum_to_reach:
				all_done = False
				break
		if all_done:
			break

		# Update
		for i in range(0, num_experiments):
			if sums[i] < sum_to_reach:
				U = random.randint(1, 6)
				sums[i] += U

# ----------------------------------------------------------------
def create_histogram_data():
	sum_to_reach = 300
	num_rolls_to_reach = 80
	num_experiments = 100000
	if len(sys.argv) == 2:
		num_experiments = int(sys.argv[1])
	for i in range(0, num_experiments):
		#print stopping_time(sum_to_reach)
		print sum_after(num_rolls_to_reach)

# ----------------------------------------------------------------
def stopping_time(sum_to_reach):
	sum = 0
	num_rolls = 0

	while sum < sum_to_reach:
		U = random.randint(1, 6)
		num_rolls += 1
		sum += U
	return num_rolls

# ----------------------------------------------------------------
def sum_after(num_rolls_to_reach):
	sum = 0
	num_rolls = 0

	while num_rolls < num_rolls_to_reach:
		U = random.randint(1, 6)
		num_rolls += 1
		sum += U
	return sum

# ----------------------------------------------------------------
main()
