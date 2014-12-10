#!/usr/bin/env python3
import example
import random
import sys
from optparse import OptionParser

class ranking:
    """
        ranking of objects and values
        
        on each insert, check if there is a element in the current
        contents which has a smaller value, if so insert the new one 
        shift the list and prune
    """
    def __init__(self,k):
        self.contents = [None]*k 

    def insert(self,value,obj):
        for idx in range(len(self.contents)):
            if self.contents[idx] == None:
                self.contents[idx] = (value,obj)
                break
            elif value <= self.contents[idx][0]:
                self.contents.insert(idx,(value,obj))
                self.contents = self.contents[0:-1]
                break
                
    def __iter__(self):
        return iter(self.contents)

def knn(k,exampleset,instance):
    """
        k-Nearest-Neighbor algorithm

        returns a ranking of size k with the k nearest neighbors
        ordered ascending by the distance to the given instance
    """
    rank_list = ranking(k)
    # execute a linear search over all examples
    for ex in exampleset:
        # do not consider examples which are set to be not active
        # this usually means that they are in the set of instances which are to be classified
        if ex.active:
            # insert the instance into the ranking of the k nearest points
            rank_list.insert(ex.euclidian_distance_to(instance),ex)
    return rank_list

def voting(rank_list):
    """
        takes a rank_list which should act like the ranking class 
        and performs a voting on the outcome 
        if there is a tie the voting is chosen as true
    """
    true  = 0
    false = 0
    # let every example in the rank_list take a vote
    for value, example in rank_list:
        if example.outcome:
            true += 1
        else:
            false += 1
    # return the majority
    return true >= false

if __name__ == "__main__":

    if sys.version_info[0] < 3 or sys.version_info[0] == 3 and sys.version_info[1] < 2:
        raise Exception('Need Python with version newer than 3.2')

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="file with examples", metavar="FILE")
    parser.add_option("-k", dest="k", help="number of nearest neighbors", metavar="NUMBER", type="int", default=1)
    (options, args) = parser.parse_args()

    es = example.ExampleSet()
    if options.filename is None:
        input_file = sys.stdin
    else:
        input_file = open(options.filename,'r')

    es.initialize_from_file(input_file)
    es.transfer_to_numerical()

    # number of instances to be chosen from the set of examples as stated by the exercise
    nbr_of_instances = 5
    instance_list = []
    for idx in random.sample(range(len(es.examples)),nbr_of_instances):
        instance_list.append(es.examples[idx])
        es.examples[idx].active = False
        es.examples.remove(es.examples[idx])

    # for each instance print the rank list as computed by k-Nearest-Neighbor
    for instance in instance_list:
        rl = knn(options.k,es,instance)
        print("++++++++++  Example {}  +++++++++".format(instance.idx))
        for value, example in rl:
            print("Example: {}, Distance {}".format(example.idx, value))
