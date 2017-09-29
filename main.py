import re
import sys
import numpy
import argparse
from pandas import read_csv
from social_choice_functions import Profile, ballot_box


def main(args):
	data = read_csv(args.input_filepath, sep='\t')  # read the data file

	mayors, voters = data.axes					 # get mayors's and voters' names
	mayors, voters = list(mayors), list(voters)	 # cast both to list

	voters_set = set([re.sub(r'\.(\d)+', '', voter) for voter in voters])  # a set of unique voters

	n_voters = len(voters)					     # number of voters
	n_single_voters = len(voters_set)  			 # number of unique voters
	n_ballot_boxes = n_voters / n_single_voters  # number of ballot boxes

	data = numpy.array(data.T)  				 # transpose

	ranks = list()								 # list of ranks
	scorer = 'profile.' + args.function 	     # voting function repr

	# For each set of voters...
	for i in range(0, n_voters, n_single_voters):
		choices = data[i:(i + n_single_voters), :]  # get choices
		profile = Profile(ballot_box(choices))	  	# create profile
		ranking = profile.ranking(eval(scorer))		# get vote ranking
		ranks.append(ranking)					    # save ranking


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	#-input FILEPATH -f FUNCTION -o FILEPATH
	parser.add_argument("-i", "--input", 
						dest="input_filepath", 
						help="Path to input file", 
						required=True)

	parser.add_argument("-f", "--function", 
						dest="function", 
						help="Social choice function",
						required=True,
						choices=['borda', 'plurality', 'simpson', 'copeland', 'dowdall', 'symmetric_borda'])

	parser.add_argument("-o", "--output", 
						dest="output_filepath", 
						default="test_output.txt", 
						help="Path to output file")

	# args.input_filepath, args.function, args.output_filepath
	args = parser.parse_args()

	main(args)