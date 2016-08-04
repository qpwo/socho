import random

class Profile(object):
    # it would save computation if I made graphs once at the start
    # todo: combine pairs that have same ballot instead of destroying one
    def __init__(self, mayors, pairs):
        self.mayors = mayors
        self.pairs = pairs

    def netPreference(self, mayor1, mayor2):
        return sum(numVotes
                   * sign(ballot.index(mayor2) - ballot.index(mayor1))
                   for (numVotes, ballot) in self.pairs)

    ## simple scores
    def copelandScore(self, mayor):
        return sum(sign(self.netPreference(mayor, mayor2))
                   for mayor2 in self.mayors)
    def symmetricBordaScore(self, mayor):
        return sum(self.netPreference(mayor, mayor2)
                   for mayor2 in self.mayors)
    def bordaScore(self, mayor):
        topScore = len(self.mayors) - 1
        return sum(numVotes * (topScore - ballot.index(mayor))
                   for numVotes, ballot in self.pairs)

    ## condorcet consistent scores
    def simpsonScore(self, mayor):
        return min(self.netPreference(mayor, mayor2)
                   for mayor2 in self.mayors - {mayor})

    ## other stuff
    def removeMayor(self, mayor):
        pass
        #return {(numVotes, removeIndex(ballot, ballot.index(candidate)))
        #        for (numVotes, ballot) in profile}

def makeRandProfile():
    ranking = range(5)
    pairs = set()
    for i in xrange(10):
        random.shuffle(ranking)
        pairs.add((random.randint(1,100),tuple(ranking)))
    return Profile(set(ranking), pairs)

def sign(n):
    return 1 if n > 0 else (-1 if n < 0 else 0)
def removeIndex(aTuple, index):
    return aTuple[:index] + aTuple[index+1:]

profile1 = Profile({0,1,2},{(102,(0,1,2)), (101,(1,2,0)), (100,(2,0,1)), (1,(2,1,0))})
profile2 = Profile({0,1,2}, {(101,(2,1,0)), (100,(0,2,1))})
profile3 = Profile({0,1,2},((40,(0,1,2)),(28,(1,2,0)),(32,(2,1,0))))
profile4 = Profile({0,1,2,3,4},{(15,(1,2,4,0,3)),(29,(0,1,3,4,2)),(42,(2,1,3,0,4)),(43,(4,1,3,2,0)),(45,(1,2,3,0,4)),(52,(3,0,1,2,4)),(53,(0,2,1,3,4)),(59,(1,2,3,4,0)),(60,(1,4,3,0,2)),(87,(1,4,0,2,3))})

### CONDORCET EXTENSIONS
#
#
#def simpsonSCF(profile):
#    _, ballot = next(iter(profile))
#    return max(ballot, key=lambda candidate: simpsonScore(profile, candidate))
#
#
### OTHER STUFF
#
#def doesParetoDominate(profile, candidate1, candidate2):
#    # assumes all pairs in profile have at least one voter
#    # todo: test if this works
#    return all(ballot.index(candidate1) < ballot.index(candidate2)
#               for _, ballot in profile)
#
#def condorcetWinner(profile):
#    _, ballot = next(iter(profile))
#    for candidate1 in ballot:
#      if any(netPreference(profile, candidate2, candidate1) > 0
#             for candidate2 in ballot):
#          next
#      else:
#          return candidate1
#    return False
#
#def singleTransferableVote(profile):
#    # messy. I think it works.
#    majority = sum(numVotes for numVotes, _ in profile) // 2 + 1
#    _, ballot = next(iter(profile))
#    votesPerCandidate = {candidate: 0 for candidate in ballot}
#    for numVotes, ballot in profile:
#        votesPerCandidate[ballot[0]] += numVotes
#
#    worstCandidate, worstNumVotes = None, float("inf")
#    for candidate, numVotes in votesPerCandidate.items():
#        if numVotes >= majority:
#            return candidate
#        if numVotes < worstNumVotes:
#            worstCandidate, worstNumVotes = candidate, numVotes
#    return singleTransferableVote(removeCandidate(profile, worstCandidate))
#
#
