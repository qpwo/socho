"""A Python implementation of some ideas in Chapter 2 of the book
Computational Choice

Authors:
Bernardo Trevizan, September 2017
Luke Miles, August 2016
Rodrigo Augusto Scheller Boos, May 2017

For more information:
https://github.com/btrevizan/pySCF
"""
import sys
import math
import copy
import numpy
from itertools import combinations, permutations

sys.setrecursionlimit(1000000)


class Profile():
    """A profile is a set of (number of votes, ballot) pairs where a
    ballot is some ordering of the candidates.

    For example:
    collectedVotes = Profile({(40,(0,1,2)),(28,(1,2,0)),(32,(2,1,0))})

    That means 40 people like candidate 0 most, then candidate 1 middle,
    and hate candidate 2. 28 people like candidate 1 the most and so on.

    Properties:
        pairs -- set of (number of votes, ballot)
        mayors -- mayors in ballots
        total_votes -- total number of votes
        net_preference_graph -- represents the preference net
        votes_per_mayor -- total votes for each mayor
    """

    def __init__(self, pairs):
        """Set the properties.

        Keyword arguments:
            pairs -- a set of votes and mayors
        """
        # Set the pairs
        self.pairs = pairs

        # Get the mayors from pairs
        # iter -- transform the set into an iterable
        it = iter(pairs)

        # next -- get the next from the iterable
        pair = next(it)

        # [1] -- mayors' index ([0] is #votes index)
        mayors = pair[1]

        # set -- convert to a set
        self.mayors = set(mayors)

        # Get the votes
        votes = [n_votes for n_votes, _ in pairs]

        # Get total number of votes
        self.total_votes = sum(votes)

        # Create a Net Preference Graph
        self.__calc_net_preference()

        # Set votes_per_mayor for Plurality
        self.__calc_votes_per_mayor()

        # Initialize a Path Preference Graph
        self.path_preference_graph = {mayor: dict() for mayor in self.mayors}

    # Mayor comparisons
    def net_preference(self, mayor1, mayor2):
        """Calculate preference between 2 mayors according to
        the Net Preference Graph and returns its answer

        Keyword arguments:
            mayor1 -- mayor to be compared
            mayor2 -- other mayor to be compared
        """
        # Get the preference in the graph
        return self.net_preference_graph[mayor1][mayor2]

    def does_pareto_dominate(self, mayor1, mayor2):
        """Returns True when mayor1 is preferred in all ballots.
        False, otherwise.

        Keyword arguments:
            mayor1 -- mayor to be compared
            mayor2 -- other mayor to be compared
        """
        # A boolean list as mayor1 preferred
        preferred = [b.index(mayor1) < b.index(mayor2)
                        for _, b in self.pairs]

        # Apply AND in all elements
        return all(preferred)

    # Simple scores
    def copeland(self, mayor):
        """Calculate the Copeland score for a mayor.

        Keyword arguments:
            mayor -- base mayor for scoring
        """
        # Get pairwise scores
        scores = list()

        for m in self.mayors:
            preference = self.net_preference(mayor, m)   # preference over m
            scores.append(numpy.sign(preference))        # win or not

        # Return the total score
        return sum(scores)

    def symmetric_borda(self, mayor):
        """Calculate the Symmetric Borda score for a mayor.

        Keyword arguments:
            mayor -- base mayor for scoring
        """
        # Get pairwise scores
        scores = [self.net_preference(mayor, m) for m in self.mayors]

        # Return the total score
        return sum(scores)

    def borda(self, mayor):
        """Calculate the Borda score for a mayor.

        Keyword arguments:
            mayor -- base mayor for scoring
        """
        # Max score to be applied with borda count
        top_score = len(self.mayors) - 1

        # Get pairwise scores
        scores = [n_votes * (top_score - ballot.index(mayor))
                    for n_votes, ballot in self.pairs]

        # Return the total score
        return sum(scores)

    def dowdall(self, mayor):
        """Calculate the Dowdall score for a mayor.

        Keyword arguments:
            mayor -- base mayor for scoring
        """
        # Max score to be applied with borda count
        top_score = len(self.mayors) - 1

        # Get pairwise scores
        scores = [n_votes * ((top_score - ballot.index(mayor)) / (ballot.index(mayor) + 1))
                    for n_votes, ballot in self.pairs]

        # Return the total score
        return sum(scores)

    def simpson(self, mayor):
        """Calculate the Simpson score for a mayor.

        Keyword arguments:
            mayor -- base mayor for scoring
        """
        # Get pairwise scores
        scores = [self.net_preference(mayor, m) for m in self.mayors - {mayor}]

        # Return the minimum score in scores
        return min(scores)

    # def plurality(self, mayor):
    #     """Calculate the Plurality score for a mayor.

    #     Keyword arguments:
    #         mayor -- base mayor for scoring
    #     """
    #     n = len(self.mayors)

    #     # Get mayors' votes by rank position
    #     for i in range(n):
    #         preference = [self.votes_per_mayor[i][mayor] >= self.votes_per_mayor[i][m]
    #                     for m in self.mayors - {mayor}]

    #         if all(preference):
    #             return n - i

    #     # Get the position with most votes
    #     return -1

    def kemeny_young(self):
        """Kemeny-Young optimal rank aggregation.

        An adaptation from:
        http://vene.ro/blog/kemeny-young-optimal-rank-aggregation-in-python.html
        """
        min_dist = numpy.inf
        best_rank = None

        n_voters = self.total_votes      # 1 vote per voter, so #votes = #voters
        n_candidates = len(self.mayors)  # #mayors = #candidates

        for rank in permutations(range(n_candidates)):

            dist = numpy.sum(self.kendalltau_dist(rank, ballot) for _, ballot in self.pairs)

            if dist < min_dist:
                min_dist = dist
                best_rank = rank

        scores_rank = list(range(n_candidates, 0, -1))
        return list(zip(best_rank, scores_rank))

    def schulze(self, mayor):
        """Return the total mayor's wins with Schulze method.

        Keyword arguments:
            mayor -- base mayor for voting count
        """
        if len(self.path_preference_graph[mayor]) == 0:  # wasn't calculated yet
            self.__calc_path_preference()

        # List of 1's and 0's (1 => win, 0 => defeat)
        wins = list()

        # For each other mayor
        for mayor2 in self.mayors - {mayor}:
            # Get strengths
            mayor1_strength = self.path_preference_graph[mayor][mayor2]
            mayor2_strength = self.path_preference_graph[mayor2][mayor]

            win_or_defeat = int(mayor1_strength > mayor2_strength)  # calculate win or defeat
            wins.append(win_or_defeat)                              # save battle's result

        # Return total number of wins
        return sum(wins)

    def ranking(self, scorer):
        """Returns a set of mayor winners according to some score function

        Keyword arguments:
            scorer -- score function (ex.: borda, copeland)
        """
        # A list of (mayor, score)
        scores = self.score(scorer)

        # Ranking is the score list ordered by score descrescent
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores

    def score(self, scorer):
        """Returns a set of mayor according to some score function.

        Keyword arguments:
            scorer -- score function (ex.: borda, copeland)
        """
        # A list of (mayor, score)
        scores = [(mayor, scorer(mayor)) for mayor in self.mayors]

        # Ranking is the score list ordered by mayor id crescent
        scores.sort(key=lambda x: x[0])

        return scores

    def winners(self, scorer):
        """Returns a set of mayor winners according to some score function

        Keyword arguments:
            scorer -- score function (ex.: borda, copeland)
        """
        ranking = self.ranking(scorer)  # get ranking
        best_score = ranking[0][1]      # get best score first tuple in ranking

        # Filter ranking to get all best score
        bests = list(filter(lambda x: x[1] == best_score, ranking))

        # Get only the mayors
        winners, scores = zip(*bests)

        # Return a set of winners
        return set(winners)

    def condorcet_winners(self):
        """Calculate the Condorcet Winners and returns a set of winner mayors"""
        winners = list()  # list of winners

        # For each mayor...
        for mayor in self.mayors:
            # If mayor beats everyone, condorcet_condition is True
            condorcet_condition = all(self.net_preference(mayor, mayor2) >= 0
                                        for mayor2 in self.mayors)

            # If True, mayor is a winner
            if condorcet_condition:
                winners.append(mayor)

        return set(winners)

    def single_transferable_vote(self, n=1):
        """Calculate the winner using Single Tranferable Voting System
        and returns a set of winner mayors.

        Keyword arguments:
            n -- number of selected winners
        """
        # Winners list
        winners = list()

        # Nth choice
        nchoice = 0

        # Calculate quota
        n_winners = n + 1                                   # used for quota
        quota = (self.total_votes // n_winners) + 1         # quota expression

        # Ranking by plurality
        ranking = self.ranking(self.plurality)

        # While there are winners to be selected (positions to be fulfilled)...
        while len(ranking) > (n - len(winners)):
            # Difference between mayor votes and quota
            quota_diff = 0              # used to redistribute the votes
            winners_len = len(winners)  # last winners length

            # For each mayor, seek winners...
            for i in range(len(ranking)):

                # Get mayor and n_votes from tuple
                mayor, n_votes = ranking[i]

                # If mayor's votes is above quota, he's a winner
                if n_votes > quota:
                    winners.append(mayor)            # update winners list
                    quota_diff += (quota - n_votes)  # add difference to quota_diff

            # If didn't found winners, remove the least popular mayor
            if winners_len == len(winners):
                quota_diff = ranking[-1][1]  # saves the number of votes
                nchoice += 1                 # update nchoice
                del ranking[-1]              # delete the last mayor (because it's ordered)

            # Distribute the deleted votes
            ranking = self.__distribute_votes(nchoice, ranking, quota_diff)

        # Fulfill the rest of the positions left
        winners += [mayor for mayor, _ in ranking]

        return set(winners)

    def sequential_majority_comparison(self):
        """Find a winner using the Sequential Majority Comparison method and
        returns the winner mayor."""
        # Create an interable from mayors set
        ordered_mayors = iter(self.mayors)

        # Get the first mayor
        last_winner = ordered_mayors.next()

        # For each mayor
        for mayor in ordered_mayors:
            # If mayor is preferred, then he's the winner
            if self.net_preference(mayor, last_winner) > 0:
                last_winner = mayor

        # Return the winner
        return last_winner

    def baldwin(self):
        """Find a winner using the Baldwin Rule and returns the winner mayor."""
        # Ranking by borda count
        ranking = self.ranking(self.borda)

        # Nth choice
        nchoice = 0

        # While there are more than 1 winner... (Yes, winner. Aren't we all?)
        while len(ranking) > 1:
            votes = ranking[-1][1]  # get least popular mayor's votes
            nchoice += 1            # update nchoice
            del ranking[-1]         # delete least popular mayor

            # Distribute the deleted votes
            ranking = self.__distribute_votes(nchoice, ranking, votes)

        # Return the remainer mayor (winner)
        return ranking[0][0]

    def nanson(self):
        """Find a winner using the Nanson Rule and returns the winner mayor."""
        # Ranking by borda count
        ranking = self.ranking(self.borda)

        # While there are more than 1 winner...
        while len(ranking) > 1:
            # Divides ranking tuples
            mayors, score = zip(*ranking)

            # Calculate borda avg score
            borda_avg = sum(score) / len(mayors)

            # For each mayor in rank...
            for i in range(len(ranking)):
                # Get mayor and its score from rank
                mayor, score = ranking[i]

                # Delete mayor rank position, if its score is below average
                if score < borda_avg:
                    del ranking[i]

        # Return the remainer mayor (winner)
        return ranking[0][0]

    def raynaud(self):
        """Find a Raynaud winner and return it."""
        # Get Simpson ranking
        simpson = self.ranking(self.simpson)

        # Return first mayor of rank
        return simpson[0][0]


    def kendalltau_dist(self, rank_a, rank_b):
        """Calculates the Kendall Tau distance.

        Keyword arguments:
            rank_a -- a ballot
            rank_b -- a ballot
        """
        tau = 0
        n_candidates = len(rank_a)

        for i, j in combinations(range(n_candidates), 2):
            tau += (numpy.sign(rank_a[i] - rank_a[j]) ==
                    -numpy.sign(rank_b[i] - rank_b[j]))

        return tau

    @staticmethod
    def plurality(probabilities, predictions):
        """Calculate the Plurality score for a mayor.

        Keyword arguments:
            probabilities -- a list of instances' probabilities,
                i.e, [ [voter's 1 instances' probabilities],
                       [voter's 2 instances' probabilities],
                       [voter's 3 instances' probabilities] ... ]
            predictions -- a list of instances' classes,
                i.e, [ [voter's 1 instances' classes],
                       [voter's 2 instances' classes],
                       [voter's 3 instances' classes] ... ]


        Score is calculated as the mean of class' probabilities.
        """
        # List of (instance, probabiliy mean) to be used as rank
        ranking = list()

        n_classifiers = len(probabilities)   # number of voters
        n_instances = len(probabilities[0])  # number of mayors

        # For each instance in every classifier...
        for i in range(n_instances):
            # Class count -> {<class>: <counts>}
            class_count = dict()

            # For each classifier...
            for c in range(n_classifiers):
                # Predicted class for instance i
                p = predictions[c][i]

                # Update the number of times the class was chosen
                class_count[p] = class_count.get(p, 0) + 1

            # Rank classes
            class_rank = sorted(class_count.items(), key=lambda x: x[1], reverse=True)

            # Most voted class for instance i
            voted_class, n_votes = class_rank[0]

            # Sum of most voted class' probabilities
            sum_probabilities = 0

            # For each classifier...
            for c in range(n_classifiers):
                # Predicted class for instance i
                if predictions[c][i] == voted_class:
                    sum_probabilities += probabilities[c][i]

            # Probability mean
            prob_mean = sum_probabilities / n_votes

            # Update ranking
            ranking.append((i, prob_mean))

        # Order ranking
        ranking.sort(key=lambda x: x[0])

        return ranking

    def __distribute_votes(self, choice, rank, votes):
        """Distribute votes keeping the proportion for each
        mayor and returns an updated rank.

        Keyword arguments:
            rank -- an ordered list of (mayor, #votes)
            votes -- number of votes to be distributed
        """
        # Get Nth choice votes per mayor
        votes_nchoice = self.votes_per_mayor[choice]

        # For each mayor...
        for i in range(len(rank)):
            mayor, n_votes = rank[i]                               # mayor and n_votes from tuple
            rate = float(votes_nchoice[mayor]) / self.total_votes  # proportion of votes
            rank[i][1] += math.floor(votes * rate)                 # updates n_votes

        # No need to reorder, because the proportion was kept
        return rank

    def __preference(self, n_votes, i, j):
        """Calculate the preference between 2 mayors and returns
        the preference according to the number fo votes.

        Keyword arguments:
            n_votes -- number of votes
            i -- index of one mayor
            j -- index of the other mayor
        """
        # Difference between mayors
        n = i - j

        # Exception: if n is equal to 0, preference is 0,
        # i.e, mayors with same index
        if n == 0:
            return 0

        # Preference is n_votes * n / abs(n)
        return n_votes * numpy.sign(n)

    def __calc_net_preference(self):
        """Create a Net Preference Graph."""

        # Create an iterable for mayors
        mayors = list(self.mayors)

        # Number of mayors
        n_mayors = len(mayors)

        # Initialize graph
        self.net_preference_graph = {mayor: dict() for mayor in mayors}

        for i in range(n_mayors):
            # Get mayor1
            mayor1 = mayors[i]

            for j in range(i, n_mayors):
                # Get mayor2
                mayor2 = mayors[j]

                # Preference list
                preferences = list()

                # For each pair of voting
                for n_votes, ballot in self.pairs:
                    k = ballot.index(mayor2)              # get the index of mayor2
                    m = ballot.index(mayor1)              # get the index of mayor1
                    p = self.__preference(n_votes, k, m)  # calculate the preference
                    preferences.append(p)                 # save preference

                # Calculate the preference
                preference = sum(preferences)

                # Save preferences
                self.net_preference_graph[mayor1][mayor2] = preference   # mayor1 VS mayor2
                self.net_preference_graph[mayor2][mayor1] = -preference  # mayor2 VS mayor1

    def __calc_votes_per_mayor(self):
        """Calculate total votes per each mayor for each rank position"""
        # Initialize structure to save the scores
        self.votes_per_mayor = list()

        # Number of mayor
        n_mayors = len(self.mayors)

        # For each mayor
        for i in range(n_mayors):
            self.votes_per_mayor.append({mayor: 0 for mayor in self.mayors})

            # For each ballot's mayor, add votes
            for n_votes, ballot in self.pairs:
                self.votes_per_mayor[i][ballot[i]] += n_votes

    def __calc_path_preference(self):
        """Calculate paths' strengths for Schulze method."""

        # Create an iterable for mayors
        mayors = list(self.mayors)

        # Number of mayors
        n_mayors = len(mayors)

        for i in range(n_mayors):
            # Get mayor1
            mayor1 = mayors[i]

            for j in range(i + 1, n_mayors):
                # Get mayor2
                mayor2 = mayors[j]

                # Get strengths
                strength1 = self.__calc_strength(mayor1, mayor2)  # mayor1 VS mayor2
                strength2 = self.__calc_strength(mayor2, mayor1)  # mayor2 VS mayor1

                # Save strengths
                self.path_preference_graph[mayor1][mayor2] = strength1
                self.path_preference_graph[mayor2][mayor1] = strength2

    def __calc_strength(self, mayor1, mayor2):
        """Return the weakest link of the strongest path.

        Keyword arguments:
            mayor1 -- origin mayor
            mayor2 -- destiny mayor
            (path from mayor1 to mayor2)
        """
        # Find possible paths between mayor1 and mayor2
        paths = self.__calc_paths(mayor1, mayor2)

        # Get strength for each path (weakest link)
        strength = list(map(lambda x: min(x), paths))

        # Return the strongest strength
        return max(strength)


    def __calc_paths(self, mayor1, mayor2, mayors=None):
        """Find the possible paths between mayor1 and mayor2.

        Keyword arguments:
            mayor1 -- origin mayor
            mayor2 -- destiny mayor
            (path from mayor1 to mayor2)
        """
        # Check if mayors exists
        if mayors is None:
            mayors = self.mayors - {mayor1}

        n_mayors = len(mayors)  # number of mayors
        paths = list()          # list of possible paths
        path = list()           # list of weights

        # For each mayor that is not mayor1...
        for mayor in mayors:

            # Get preference of mayor1 over mayor
            preference = self.net_preference_graph[mayor1][mayor]
            path.append(preference)  # save current weigth

            # End of path
            if mayor == mayor2:
                paths.append(path)       # add to possible paths
                path = list()            # start a new path
            else: # path isn't over
                new_mayors = mayors - {mayor}
                subpath = self.__calc_paths(mayor, mayor2, new_mayors)

                # For each subpath (list of weights),
                # concatenate with current path and save it
                for weights in subpath:
                    paths.append(path + weights)

        # Return a list of possible paths between mayor1 and mayor2
        return paths

    def _build_graph(self):
        """Build graph for Kemeny-Young method.

        An adaptation from:
        http://vene.ro/blog/kemeny-young-optimal-rank-aggregation-in-python.html
        """
        n_voters = self.total_votes
        n_candidates = len(self.mayors)

        ranks = list()
        for n_votes, ballot in self.pairs:
            for i in range(n_votes):
                ranks.append(list(ballot))

        ranks = numpy.array(ranks)
        edge_weights = numpy.zeros((n_candidates, n_candidates))

        for i, j in combinations(range(n_candidates), 2):
            preference = ranks[:, i] - ranks[:, j]

            h_ij = numpy.sum(preference < 0)  # prefers i to j
            h_ji = numpy.sum(preference > 0)  # prefers j to i

            if h_ij > h_ji:
                edge_weights[i, j] = h_ij - h_ji
            elif h_ij < h_ji:
                edge_weights[j, i] = h_ji - h_ij

        return edge_weights

    @classmethod
    def ballot_box(cls, choices):
        """Index and order choices for Profile.

        Keyword arguments:
            choices -- a list of ranked mayors,
            i.e, [ [voter's 1 ranked mayors],
                   [voter's 2 ranked mayors],
                   [voter's 3 ranked mayors] ... ]

        Return type:
            A set of (number of votes, mayors ranked)
        """
        n_voters = len(choices)  # number of voters

        if not (type(choices[0][0]) is tuple): # it's not indexed
            # INDEX CHOICES, i.e., name mayors
            # For each classification, create [(mayor1, rank1), (mayor2, rank2)...]
            choices = list(map(lambda x: list(enumerate(x)), choices))

        # ORDER each classification in decrescent order
        choices = list(map(lambda x: sorted(x, key=lambda y: y[1], reverse=True), choices))

        # GROUP choices with same ordering (same preference order)
        # Empty dict for save pairs -> {'preference order': number of voters}
        ballots = dict()

        # For each classification...
        for i in range(n_voters):
            key, _ = zip(*choices[i])  # get only mayors' names as key
            key = tuple(key)           # cast to tuple to use as dict's key

            # Counts the classifications with same ordering
            ballots[key] = ballots.get(key, 0) + 1

        # DATA FOR PROFILE
        # Pairs -> [(ballot, number of votes)...]
        pairs = list(ballots.items())

        # Transform -> [(number of votes, ballot)...]
        pairs = list(map(lambda x: (x[1], x[0]), pairs))

        # Cast to set and return as a Profile
        return cls(set(pairs))

    @classmethod
    def aggr_rank(cls, probabilities, sc_functions, predictions=[]):
        """Aggregate probabilities and return a ranking.

        Keyword arguments:
            probabilities -- a list of instances' probabilities,
                i.e, [ [voter's 1 instances' probabilities],
                       [voter's 2 instances' probabilities],
                       [voter's 3 instances' probabilities] ... ]
            sc_functions -- a list with the name of social choice functions
            predictions -- a list of instances' predictions (default []),
                i.e, [ [voter's 1 instances' predictions],
                       [voter's 2 instances' predictions],
                       [voter's 3 instances' predictions] ... ]
        """
        profile = cls.ballot_box(probabilities)
        rankings = dict()

        for scf in sc_functions:

            if scf == 'plurality':
                rank = profile.plurality(probabilities, predictions)
            elif scf == 'kemeny_young':
                rank = profile.kemeny_young()
            else:
                rank = profile.score(eval('profile.' + scf))

            rankings[scf] = rank

        return rankings
