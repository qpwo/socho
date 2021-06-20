# socho

As in python **So**cial **Cho**ice Function. `social_choice_functions.py` has the class
`Profile`, as in a voting profile. Then there are methods to get the best
candidate in a profile, or to get the score of an individual candidate.

A profile is a `set` of `(number of votes, ballot)` pairs where a ballot is
some ordering of the candidates. For example:

`collectedVotes = Profile({(40,(0,1,2)),(28,(1,2,0)),(32,(2,1,0))})`

That means 40 people like candidate 0 most, then candidate 1 middle, and hate
candidate 2.  28 people like candidate 1 the most and so on.

If your set of candidates is `S`, then each the ballot should contain each
element in `S` exactly once, in any order.  Your candidates can be any hashable
objects.

`weirdProfile = Profile({(40,(2,1,56.78)),(28,(1,56.78,2)),(32,(56.78,1,2))})`

```
>>> weirdProfile.mayors
set(56.78, 1, 'fish')
```

And of course you can run elections:

```
>>> weirdProfile.singleTransferableVote()
set([56.78])
```

## Installation
```bash
$ pip3 install social-choice
```

## Getting Started
```python
from socho.profile import Profile, ballot_box, plurality

ballots = [(2,1,56.78), (2,1,56.78), (2,1,56.78), (1,56.78,2), (1,56.78,2), (56.78,1,2), (56.78,1,2)]

# Create a profile
profile = Profile.ballot_box(ballots)
scorer = profile.borda  # function to calculate score for each mayor

# A mayor list ranked by score
# [(2, 10), (0, 7), (1, 4)]
# maps to [(56.78, 10), (1, 7), (2, 4)]
rank = profile.ranking(scorer)

# 56.78 is the winner
# 1 as 2nd place
# 2 as 3rd place
```

## Command Line Usage
```bash
usage: main.py [-h] -i INPUT_FILEPATH [-p PREDICTIONS_FILEPATH] [-s SEP] -f
               {borda,plurality,simpson,copeland,dowdall,symmetric_borda}
               [-o OUTPUT_FILEPATH] [-c COMPARE_FILEPATH]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILEPATH, --input INPUT_FILEPATH
                        Path to input file.
  -p PREDICTIONS_FILEPATH, --predictions PREDICTIONS_FILEPATH
                        Path to predictions file (required for plurality).
  -s SEP, --sep SEP     File separator, i. e., ',' or ' '...
  -f {borda,plurality,simpson,copeland,dowdall,symmetric_borda}, --function {borda,plurality,simpson,copeland,dowdall,symmetric_borda}
                        Social choice function.
  -o OUTPUT_FILEPATH, --output OUTPUT_FILEPATH
                        Path to output file.
  -c COMPARE_FILEPATH, --compare COMPARE_FILEPATH
                        Path to rank file to be compared.
```

### Example
```bash
$ python3 main.py -i tests/input.txt -f borda -o tests/output.txt
```

### Test files
Examples of input and output files are in `tests/` folder. Please follow the same structure.

## Methods
- Baldwin -> winner
- Borda -> ranking
- Condorcet -> set of winners
- Copeland -> ranking
- Dowdall -> ranking
- Kemeny Young -> ranking
- Nanson -> winner
- Pareto's check -> boolean
- Plurality -> ranking
- Raynaud -> winner
- Schulze -> ranking
- Sequential Majority Comparison -> winner
- Simpson -> ranking
- Symmetric Borda -> ranking
- Single Transferable Vote -> set of winners

# Note
The Kemeny Young method's complexity is O(n!). So, be careful with your input.
