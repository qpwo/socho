import numpy
import argparse

from pandas import read_csv
from social_choice_functions import Profile, ballot_box


def main(args):
	data = read_csv(args.input_filepath, sep=args.sep)  # read the data file
	
	mayors = data.axes[0]								# line labels (mayors)
	mayors = list(mayors)								# cast to list

	# (mayors X votes) to (votes X mayors)
	data = numpy.array(data.T)  				    	# transpose

	profile = Profile(ballot_box(data))	  			# create profile
	scorer = eval('profile.' + args.function) 	     	# voting method
	ranking = profile.ranking(scorer)					# get ranking

	# Map back to mayors labels
	for i in range(len(ranking)):
		j = ranking[i][0]						 	 # get mayor index
		mayors_label = "\"{}\"".format(mayors[j])    # mayors name
		ranking[i] = (mayors_label, ranking[i][1])	 # save mayor label

	# Save rank in file
	output = open(args.output_filepath, 'w')

	for mayor, score in ranking:
		output.write("{} {}\n".format(mayor, score))

	output.close()

	# If file to compare ranking exists...
	if not (args.compare_filepath is None):
		print("Comparing with {}...".format(args.compare_filepath))

		compare = open(args.compare_filepath, 'r')  # open file
		line_count = 1								# for error msg
		error_count = 0								# for error counting

		# For each ranked position...
		for mayor1, score1 in ranking:
			line = compare.readline()  		  # get position to compare
			mayor2, score2 = line.split(' ')  # split info

			# Print message if it is different
			if mayor1 != mayor2:
				print("{} should be {} in line {}".format(mayor1, mayor2, line_count))
				error_count += 1  # update error count

			line_count += 1

		compare.close()

		print("{} errors of {}.".format(error_count, line_count-1))


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