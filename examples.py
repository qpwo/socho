from social_choice_functions import Profile

# making a few instances of the class.
profile1=Profile({(102,(0,1,2)),(101,(1,2,0)),(100,(2,0,1)),(1,(2,1,0))})
profile2=Profile({(101,(2,1,0)),(100,(0,2,1))})
profile3=Profile({(40,(0,1,2)),(28,(1,2,0)),(32,(2,1,0))})
profile4=Profile({(15,(1,2,4,0,3)),(29,(0,1,3,4,2)),(42,(2,1,3,0,4)),(43,(4,1,3,2,0)),(45,(1,2,3,0,4)),(52,(3,0,1,2,4)),(53,(0,2,1,3,4)),(59,(1,2,3,4,0)),(60,(1,4,3,0,2)),(87,(1,4,0,2,3))})
profile5=Profile({(20,(0,1,2)),(20,(1,2,0)),(20,(2,0,1))})
profile6=Profile({(10,(0,1,2)),(10,(0,2,1))})

# showing some of the properties and methods of an instance
print profile4.mayors
print profile4.pairs
print profile4.netPreference(3,2)
print profile4.simpsonScore(1)
print profile4.bordaScore(4)
print profile4.pluralityRule()
print profile4.smallestRule()
print profile3.singleTransferableVote()
print profile6.doesParetoDominate(0,1)
print profile6.doesParetoDominate(2,1)
