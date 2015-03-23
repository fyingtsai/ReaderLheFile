#!/usr/bin/python2.7
# Author: Kelly Tsai
import sys
reload(sys)

Str = 'Integrated weight (pb)'

def getIntegratedWeight(filename):
	with open(filename,'r') as f:
		for line in f:
			if line.find(Str) > 0:
				weightValue = line.split(' : ')[1]
				return weightValue


def main():
	try:
		print getIntegratedWeight(sys.argv[1])
	except:
		print 'command-line arguments:'
		print 'python FileName.py BeReadFile'

if __name__ == "__main__":
   main()