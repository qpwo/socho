# Luke Miles, August 2016
# a python implementation of some ideas in chapter 2 of the book Computational Choice

from __future__ import division
import random

class Profile(object):
    # todo: combine identical pairs instead of destroying one

    def __init__(self, pairs):
        self.pairs = pairs
        self.mayors = set(next(iter(pairs))[1])
        self.totalVotes = sum(numVotes for (numVotes, _) in pairs)
        self.netPreferenceGraph = {mayor: dict() for mayor in self.mayors}
        self.votesPerMayor = None

    ## mayor comparisons
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
    def pluralityScore(self, mayor):
        if self.votesPerMayor is not None:
            return self.votesPerMayor[mayor]
        else:
            self.votesPerMayor = {mayor: 0 for mayor in self.mayors}
            for numVotes, ballot in self.pairs:
                self.votesPerMayor[ballot[0]] += numVotes
            return self.votesPerMayor[mayor]

    ## social choice functions
    def scoreWinners(self, scoreFunction):
        return set(maxes(self.mayors, key=scoreFunction))
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
                return {mayor}
            if numVotes < worstNumVotes:
                worstMayor, worstNumVotes = mayor, numVotes
        return self.removeMayor(worstMayor).singleTransferableVote()
    def sequentialMajorityComparison(self):
        orderedMayors = iter(self.mayors)
        lastWinner = orderedMayors.next()
        for mayor in orderedMayors:
            print "checking mayor", mayor
            if self.netPreference(mayor, lastWinner) > 0:
                lastWinner = mayor
            print "current winner is", lastWinner
        return lastWinner
    def baldwinRule(self):
        if len(self.mayors) == 1:
            return self.mayors
        worstMayor = min(self.mayors, key=self.bordaScore)
        return self.removeMayor(worstMayor).baldwinRule()
    def nansonRule(self):
        if len(self.mayors) == 1:
            return self.mayors
        bordaScores = {mayor: self.bordaScore(mayor) for mayor in self.mayors}
        averageBordaScore = sum(bordaScores.values()) / len(self.mayors)
        badMayors = {mayor for mayor in self.mayors
                     if bordaScores[mayor] < averageBordaScore}
        if not badMayors:
            return self.mayors
        nextProfile = self
        for mayor in badMayors:
            nextProfile = nextProfile.removeMayor(mayor)
        return nextProfile.nansonRule()


    ## other stuff
    def removeMayor(self, mayor):
        return Profile({(numVotes, removeIndex(ballot, ballot.index(mayor)))
                for (numVotes, ballot) in self.pairs})

def makeRandProfile(numMayors, numBallots, maxNumVotes):
    ranking = range(numMayors)
    pairs = set()
    for i in xrange(numBallots):
        random.shuffle(ranking)
        pairs.add((random.randint(1,maxNumVotes),tuple(ranking)))
    return Profile(pairs)

def sign(n):
    return 1 if n > 0 else (-1 if n < 0 else 0)
def removeIndex(aTuple, index):
    return aTuple[:index] + aTuple[index+1:]
def maxes(iterable, key=lambda x: x):
    keyOfBest = None
    bests = []
    for item in iterable:
        keyOfItem = key(item)
        if keyOfItem > keyOfBest or keyOfBest is None:
            bests = [item]
            keyOfBest = keyOfItem
        elif keyOfItem == keyOfBest:
            bests.append(item)
    return bests
