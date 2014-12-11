#!/usr/bin/env python3
import sys
from optparse import OptionParser
from random import randint
from random import shuffle

if sys.version_info[0] < 3 or sys.version_info[0] == 3 and sys.version_info[1] < 2:
	raise Exception('Need Python with version newer than 3.2')

""" generate an Example set with nPosExamples positive examples and a cardinality of SetCardinality """
def generateExampleSet(SetCardinality, nPosExamples):
	S = [0]*SetCardinality
	for i in range(0,nPosExamples):
		rindex = randint(0, SetCardinality-1)		
		while S[rindex] == 1:		
			rindex = randint(0, SetCardinality-1)
		S[rindex] = 1
	return S

""" generate a random permutation of the Set S """
def generateRandomPermutation(S):
	pi = list(S)
	shuffle(pi)
	return pi

""" generate a random permutation of the Set S, where number of positive examples nPosExamples are located in the first/last
m indices, depending on m being positive or negative
( actually new Example Set is created, prob. for hitting a satisfying random permutation with shuffling is low ) """
def generateRandomPermutationFrontBack(S, m, nPosExamples):	
	pi = [0]*len(S)
	for i in range(0,nPosExamples):
		rindex = randint(0, abs(m)-1)
		while pi[rindex] == 1:		
			rindex = randint(0, abs(m)-1)
		pi[rindex] = 1
	if m<0:
		pi.reverse()
	return pi
			
	
""" construct an approximation for ROC from Set S and calculate area under curve by
summation over deltaX * y[i] """
def calculateAUC(S, SetCardinality, nPosExamples):
	# construct approx. for ROC
	nNegExamples = SetCardinality - nPosExamples	
	values = [[0, 0]]	
	for example in S:
		if example == 0:
			values.append([values[-1][0]+1/nNegExamples, values[-1][1]])
		else:
			values.append([values[-1][0], values[-1][1]+1/nPosExamples])
	# calc area under curve
	area = 0	
	for i in range(1, len(values)-1):
		deltaX = values[i][0]-values[i-1][0]
		area += deltaX*values[i][1]
	return area

if __name__ == "__main__":
	SetCardinality = 1000
	nPosExamples = 10
	S = generateExampleSet(SetCardinality, nPosExamples)
	
	print("\npart (b):")	
	for i in range(1,11):	
		pi = generateRandomPermutation(S)
		area = calculateAUC(pi, SetCardinality, nPosExamples)
		print ("area experiment #{0:2}: {1}".format(i, area))
	
	print("\npart (c):")
	M = [500, 100, 50, 25, 20, 15, 10]
	for m in M:
		pi = generateRandomPermutationFrontBack(S, m, nPosExamples)
		areaForward = calculateAUC(pi, SetCardinality, nPosExamples)
		pi = generateRandomPermutationFrontBack(S, -m, nPosExamples)
		areaBackward = calculateAUC(pi, SetCardinality, nPosExamples)
		print ("area experiment pi_m={0:3} (front of pi/back of pi): {1} / {2}".format(m, areaForward, areaBackward))
