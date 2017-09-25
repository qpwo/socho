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

There are a bunch of examples in `examples.py`. The code is pretty readable, so
to really get it look in `social_choice_functions.py`.

# Methods
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
