#!/usr/bin/env python3
import knn
import example
import sys
from confusion_matrix import ConfusionMatrix
from optparse import OptionParser

if sys.version_info[0] < 3 or sys.version_info[0] == 3 and sys.version_info[1] < 2:
    raise Exception('Need Python with version newer than 3.2')

def leave_one_out(examples,k):
    conf_matr = ConfusionMatrix()
    for ex in examples:
        # disable only this example
        ex.active = False
        # run the k-Nearest-Neighbor algorithm
        rank_list = knn.knn(k,examples,ex)
        # check the voting for correctness
        outcome = knn.voting(rank_list)
        conf_matr.inc_according_to(outcome,ex.outcome)
        ex.active = True
    # return the computed confusion matrix
    return conf_matr

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="file with examples", metavar="FILE")
    parser.add_option("-k", dest="k", help="number of nearest neighbors", metavar="NUMBER", type="int", default=1)
    parser.add_option("-a", "--alpha", dest="alpha", help="alpha-value for f-measure", metavar="NUMBER", type="float", default=1.0)
    (options, args) = parser.parse_args()

    es = example.ExampleSet()
    if options.filename is None:
        input_file = sys.stdin
    else:
        input_file = open(options.filename,'r')
    es.initialize_from_file(input_file)
    es.transfer_to_numerical()

    conf_matr = leave_one_out(es,options.k)
    print("Precision: {}".format(conf_matr.get_precision()))
    print("Recall: {}".format(conf_matr.get_recall()))
    print("F-Measure (with alpha={}): {}".format(options.alpha, conf_matr.get_f_measure(options.alpha)))
    print("Accuracy: {}".format(conf_matr.get_accuracy()))
