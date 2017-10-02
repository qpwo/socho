# pySCF

As in python Social Choice Function. `social_choice_functions.py` has the class
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

`weirdProfile = Profile({(40,("fish",1,56.78)),(28,(1,56.78,"fish")),(32,(56.78,1,"fish"))})`

```
>>> weirdProfile.mayors
set(56.78, 1, 'fish')
```

And of course you can run elections:

```
>>> weirdProfile.singleTransferableVote()
set([56.78])
```

## Usage
```bash
usage: main.py [-h] -i INPUT_FILEPATH [-s SEP] -f
               {borda,plurality,simpson,copeland,dowdall,symmetric_borda}
               [-o OUTPUT_FILEPATH] [-c COMPARE_FILEPATH]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILEPATH, --input INPUT_FILEPATH
                        Path to input file.
  -s SEP, --sep SEP     File separator, i. e., ',' or ' '...
  -f {borda,plurality,simpson,copeland,dowdall,symmetric_borda}, --function {borda,plurality,simpson,copeland,dowdall,symmetric_borda}
                        Social choice function.
  -o OUTPUT_FILEPATH, --output OUTPUT_FILEPATH
                        Path to output file.
  -c COMPARE_FILEPATH, --compare COMPARE_FILEPATH
                        Path to rank file to be compared.
```

## Example
```bash
$ python3 main.py -i tests/input.txt -f borda -o tests/output.txt
```

### Test files
Examples of input and output files are in `tests/` folder. Please follow the same structure.

## Methods
- Borda Count
- Single Transferable Vote
- Sequential Majority Comparison
- Plurality
- Baldwin's Rule
- Pareto's check
- Simpson
- Nanson's Rule
- Condorcet
- Copeland
- Symmetric Borda
- Dowdall
- Schulze
