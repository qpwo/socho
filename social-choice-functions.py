# Luke Miles 2016-08-02
# Writing functions from section 2.2 of the book "Computational Choice"

#myProfile = {(102,(0,1,2)), (101,(1,2,0)), (100,(2,0,1)), (1,(2,1,0))}
#myProfile = {(100,(2,1,0)), (100,(0,2,1))}

# 0 is trump, 1 is bernie, 2 is hillary
#myProfile = {(40,(0,1,2)),(28,(1,2,0)),(32,(2,1,0))}

def sign(n):
    return 1 if n > 0 else (-1 if n < 0 else 0)

def netPreference(profile, candidate1, candidate2):
    return sum(numVoters
               * sign(ballot.index(candidate2) - ballot.index(candidate1))
               for (numVoters, ballot) in profile)

## SIMPLE SCORES

def copelandScore(profile, candidate):
    _, ballot = next(iter(profile))
    return sum(sign(netPreference(profile, candidate, aCandidate))
               for aCandidate in ballot)

def symmetricBordaScore(profile, candidate):
    _, ballot = next(iter(profile))
    return sum(netPreference(profile, candidate, aCandidate)
               for aCandidate in ballot)

def asymmetricBordaScore(profile, candidate):
    _, ballot = next(iter(profile))
    topScore = len(ballot) - 1
    return sum(numVoters * (topScore - ballot.index(candidate))
               for numVoters, ballot in profile)

## OTHER STUFF

def doesParetoDominate(profile, candidate1, candidate2):
    # assumes all pairs in profile have at least one voter
    # todo: test if this works
    return all(ballot.index(candidate1) < ballot.index(candidate2)
               for _, ballot in profile)

def condorcetWinner(profile):
    _, ballot = next(iter(profile))
    for candidate1 in ballot:
      if any(netPreference(profile, candidate2, candidate1) > 0
             for candidate2 in ballot):
          next
      else:
          return candidate1
    return False

def singleTransferableVote(profile):
    # messy. I think it works.
    majority = sum(numVoters for numVoters, _ in profile) // 2 + 1
    _, ballot = next(iter(profile))
    votersPerCandidate = {candidate: 0 for candidate in ballot}
    for numVoters, ballot in profile:
        votersPerCandidate[ballot[0]] += numVoters

    worstCandidate, worstNumVotes = None, float("inf")
    for candidate, numVoters in votersPerCandidate.items():
        if numVoters >= majority:
            return candidate
        if numVoters < worstNumVotes:
            worstCandidate, worstNumVotes = candidate, numVoters
    return singleTransferableVote(removeCandidate(profile, worstCandidate))

def removeCandidate(profile, candidate):
    # current bug: if two pairs in profile are made identical by the removal
    # of candidate, then one copy is destroyed
    return {(numVoters, removeIndex(ballot, ballot.index(candidate)))
            for (numVoters, ballot) in profile}

def removeIndex(aTuple, index):
    return aTuple[:index] + aTuple[index+1:]


## CONDORCET EXTENSIONS

def simpsonScore(profile, candidate):
    ballot = set(next(iter(profile))[1]) - {candidate}
    return min(netPreference(profile, candidate, candidate2)
               for candidate2 in ballot)

def simpsonSCF(profile):
    _, ballot = next(iter(profile))
    return max(ballot, key=lambda candidate: simpsonScore(profile, candidate))

