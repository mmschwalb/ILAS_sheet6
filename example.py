#!/usr/bin/env python3
import string
import sys
import math

class Example:
    """
    example
    """
    def __init__(self,value_hash,outcome):
        self.value_hash = value_hash
        self.outcome    = outcome
        self.active     = True
        self.idx        = None

    def __str__(self):
        return str(self.value_hash) + "------------" + str(self.outcome)

    def euclidian_distance_to(self,other):
        ret = 0
        self_values  = list(self.value_hash.values())
        other_values = list(other.value_hash.values())
        for idx in range(len(self_values)):
            ret += math.pow((self_values[idx] - other_values[idx]),2)
        return math.sqrt(ret)

class ExampleSet:
    """
    Containes a set of examples this includes the variables

        * examples: a list of all contained examples
        * negatives: the total number of examples with positive outcome
        * positives: the total number of examples with negative outcome
    """
    def __init__(self,examples = []):
        self.examples  = []
        self.positives = 0
        self.negatives = 0

    def initialize_from_file(self,input_file):
        """
        initialize this example set from a file as specified by the exercise
        """
        # read the first line with attributes 
        init_line = input_file.readline()
        #  and parse this line into attribute name and type
        self.attributes = { x[0] : x[1] for x in list(map(lambda s : [s[0],s.rstrip()[-1]], init_line.split(',')))[0:-1]}

        # parse the rest of the file containing the examples
        self.examples = []
        self.positives = 0
        self.negatives = 0
        for line in input_file:
            example_list = list(map(lambda s : s.rstrip() , line.split(',')))
            example_hash = dict(zip(sorted(self.attributes),example_list))
            for key in example_hash.keys():
                if self.attributes[key] == 'n':# convert all numerical values from str to float
                    example_hash[key] = float(example_hash[key])
                elif self.attributes[key] == 'b': # and all boolean values from str to boolean
                    example_hash[key] = (example_hash[key] == "yes")
                elif self.attributes[key] == 'c':
                    example_hash[key] = example_hash[key][-1]

            new_example = Example(example_hash,example_list[-1] == "yes")
            new_example.idx = len(self.examples)
            self.examples.append(new_example)
            if example_list[-1] =="yes":
                self.positives += 1
            else:
                self.negatives += 1

    def transfer_to_numerical(self):
        """
        transfer all non-numerical attributes to numerical attributes
        """
        for example in self.examples:
            for a_key in example.value_hash.keys():
                if self.attributes[a_key] == 'c':
                    example.value_hash[a_key] = ord(example.value_hash[a_key])-96
                elif self.attributes[a_key] == 'b':
                    example.value_hash[a_key] = 1 if example.value_hash[a_key] else 0
        for a_key in self.attributes.keys():
            self.attributes[a_key] = 'n'


    def __iter__(self):
        return iter(self.examples)

