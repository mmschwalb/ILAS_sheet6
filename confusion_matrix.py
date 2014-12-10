#!/usr/bin/env python3

class ConfusionMatrix:
    def __init__(self):
        self.true_positives  = 0
        self.false_positives = 0
        self.true_negatives  = 0
        self.false_negatives = 0

    def inc_according_to(self,outcome,true_outcome):
        if not type(outcome) is type(true_outcome):
            raise Exeption()
        if type(outcome) is int:
            if outcome>0:
                if true_outcome>0:
                    self.inc_tp()
                else:
                    self.inc_fp()
            else:
                if true_outcome==0:
                    self.inc_tn()
                else:
                    self.inc_fn()
        if type(outcome) is bool:
            if outcome:
                if true_outcome:
                    self.inc_tp()
                else:
                    self.inc_fp()
            else:
                if not true_outcome:
                    self.inc_tn()
                else:
                    self.inc_fn()


    def inc_tp(self):
        self.true_positives += 1

    def inc_fp(self):
        self.false_positives += 1

    def inc_tn(self):
        self.true_negatives += 1

    def inc_fn(self):
        self.false_negatives += 1

    def get_precision(self):
        return float(self.true_positives)/(self.true_positives + self.false_positives)

    def get_recall(self):
        return float(self.true_positives)/(self.true_positives + self.false_negatives)

    def get_f_measure(self,alpha):
        denominator = alpha*(1/self.get_precision()) + (1-alpha)*(1/self.get_recall())
        return 1/denominator

    def get_accuracy(self):
        total = self.true_positives + self.false_positives
        total += self.true_negatives + self.false_negatives
        return (self.true_positives + self.true_negatives)/float(total)
