import numpy
import argparse

from pandas import read_csv
from social_choice_functions import Profile, ballot_box


def main(args):
	data = read_csv(args.input_filepath, sep=args.sep)  # read the data file
	data = numpy.array(data.T)  				    	# transpose

	profile = Profile(ballot_box(choices))	  			# create profile
	scorer = eval('profile.' + args.function) 	     	# voting method
	ranking = profile.ranking(scorer)					# get ranking

	# Map to instances names
	# Save
	# Compare


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	#-input FILEPATH -f FUNCTION -o FILEPATH
	parser.add_argument("-i", "--input", 
						dest="input_filepath", 
						help="Path to input file.", 
						required=True)

	parser.add_argument("-s", "--sep", 
						dest="sep",
						default="\t",
						help="File separator, i. e., ',' or '\t'...")

	parser.add_argument("-f", "--function", 
						dest="function", 
						help="Social choice function.",
						required=True,
						choices=['borda', 'plurality', 'simpson', 'copeland', 'dowdall', 'symmetric_borda'])

	parser.add_argument("-o", "--output", 
						dest="output_filepath", 
						default="test_output.txt", 
						help="Path to output file.")

	parser.add_argument("-c", "--compare", 
						dest="compare_filepath", 
						default=None, 
						help="Path to rank file to be compared.")

	args = parser.parse_args()
	main(args)