#!/usr/bin/env python3
import sys
from optparse import OptionParser
from random import randint
from random import shuffle

if sys.version_info[0] < 3 or sys.version_info[0] == 3 and sys.version_info[1] < 2:
	raise Exception('Need Python with version newer than 3.2')

def generateExampleSet(setCardinality, nPosExamples):
	S = [0]*setCardinality
	for i in range(0,nPosExamples):
		rindex = randint(0, setCardinality-1)		
		while S[rindex] == 1:		
			rindex = randint(0, setCardinality-1)
		S[rindex] = 1
	return S

def generateRandomPermutation(S):
	pi = list(S)
	shuffle(pi)
	return pi

def generateRandomPermutationFrontBack(S, m, nPosExamples):
	pi = generateRandomPermutation(S)
	if m>0:
		# not enough positives in range, get new permutation!		
		while sum(pi[0:m]) < nPosExamples:
			pi = generateRandomPermutation(S)
	else:
		# same, but from the end of pi		
		while sum(pi[-0:m]) < nPosExamples:
			pi = generateRandomPermutation(S)
	return pi
			
	
def calculateAUC(S, setCardinality, nPosExamples):
	# construct approx. for ROC
	nNegExamples = setCardinality - nPosExamples	
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
	setCardinality = 1000
	nPosExamples = 10
	S = generateExampleSet(setCardinality, nPosExamples)
	
	print("\npart (b):")	
	for i in range(1,11):	
		pi = generateRandomPermutation(S)
		area = calculateAUC(pi, setCardinality, nPosExamples)
		print ("area experiment #{0:2}: {1}".format(i, area))
	
	print("\npart (c):")
	M = [500, 100, 50, 25, 20, 15, 10]
	for m in M:
		pi = generateRandomPermutationFrontBack(S, m, nPosExamples)
		areaForward = calculateAUC(pi, setCardinality, nPosExamples)
		pi = generateRandomPermutationFrontBack(S, -m, nPosExamples)
		areaBackward = calculateAUC(pi, setCardinality, nPosExamples)
		print ("area experiment pi_m={0:3} (front of pi/back of pi): {1} / {2}".format(m, areaForward, areaBackward))

