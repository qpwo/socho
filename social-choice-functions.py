import random

class Profile(object):
    # todo: combine identical pairs instead of destroying one
    def __init__(self, pairs):
        self.pairs = pairs
        self.mayors = set(next(iter(pairs))[1])
        self.totalVotes = sum(numVotes for (numVotes, _) in pairs)
        self.netPreferenceGraph = {mayor: dict() for mayor in self.mayors}
        self.votesPerMayor = None

    def netPreference(self, mayor1, mayor2):
        try:
            return self.netPreferenceGraph[mayor1][mayor2]
        except KeyError:
            answer = sum(numVotes
                         * sign(ballot.index(mayor2) - ballot.index(mayor1))
                         for (numVotes, ballot) in self.pairs)
            self.netPreferenceGraph[mayor1][mayor2] = answer
            self.netPreferenceGraph[mayor2][mayor1] = -answer
            return answer
    def numTopVotes(self, mayor):
        if self.votesPerMayor is not None:
            return self.votesPerMayor[mayor]
        else:
            self.votesPerMayor = {mayor: 0 for mayor in self.mayors}
            for numVotes, ballot in self.pairs:
                self.votesPerMayor[ballot[0]] += numVotes
            return self.votesPerMayor[mayor]
    def doesParetoDominate(self, mayor1, mayor2):
        return all(ballot.index(mayor1) < ballot.index(mayor2)
                   for _, ballot in self.pairs)

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
    def simpsonScore(self, mayor):
        return min(self.netPreference(mayor, mayor2)
                   for mayor2 in self.mayors - {mayor})

    ## a few social choice functions
    def pluralityRule(self):
        return max(self.mayors, key=self.numTopVotes)
    def smallestRule(self):
        return min(self.mayors, key=self.numTopVotes)
    def condorcetWinners(self):
        return {mayor for mayor in self.mayors
                if all(self.netPreference(mayor, mayor2)>=0
                       for mayor2 in self.mayors)}
    def singleTransferableVote(self):
        votesPerMayor = {mayor: 0 for mayor in self.mayors}
        for numVotes, ballot in self.pairs:
            votesPerMayor[ballot[0]] += numVotes
        worstMayor, worstNumVotes = None, float("inf")
        for mayor, numVotes in votesPerMayor.items():
            if numVotes > self.totalVotes//2:
                return mayor
            if numVotes < worstNumVotes:
                worstMayor, worstNumVotes = mayor, numVotes
        return self.removeMayor(worstMayor).singleTransferableVote()

    ## other stuff
    def removeMayor(self, mayor):
        return Profile({(numVotes, removeIndex(ballot, ballot.index(mayor)))
                for (numVotes, ballot) in self.pairs})

def makeRandProfile(numMayors, numBallots):
    ranking = range(numMayors)
    pairs = set()
    for i in xrange(numBallots):
        random.shuffle(ranking)
        pairs.add((random.randint(1,100),tuple(ranking)))
    return Profile(pairs)

def sign(n):
    return 1 if n > 0 else (-1 if n < 0 else 0)
def removeIndex(aTuple, index):
    return aTuple[:index] + aTuple[index+1:]

profile1=Profile({(102,(0,1,2)),(101,(1,2,0)),(100,(2,0,1)),(1,(2,1,0))})
profile2=Profile({(101,(2,1,0)),(100,(0,2,1))})
profile3=Profile({(40,(0,1,2)),(28,(1,2,0)),(32,(2,1,0))})
profile4=Profile({(15,(1,2,4,0,3)),(29,(0,1,3,4,2)),(42,(2,1,3,0,4)),(43,(4,1,3,2,0)),(45,(1,2,3,0,4)),(52,(3,0,1,2,4)),(53,(0,2,1,3,4)),(59,(1,2,3,4,0)),(60,(1,4,3,0,2)),(87,(1,4,0,2,3))})
profile5=Profile({(20,(0,1,2)),(20,(1,2,0)),(20,(2,0,1))})
profile6=Profile({(10,(0,1,2)),(10,(0,2,1))})


