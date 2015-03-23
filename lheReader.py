#!/usr/bin/python2.7
# Author: Kelly Tsai

import sys
import glob
import errno

class GetValue():
    def __init__(self):
    	self.zpMass = []
    	self.weight = []
    	self.tanBeta = []

lheWeightList = []
lheZpMassList = []
Str = 'Integrated weight (pb)'
path = '/Users/KellyTsai/Documents/MadGraph/Zp_hA0_bb_hleFile/*.lhe'   
files = glob.glob(path) 

def store_ZpMass(fileName):
		mass = str(fileName).split("events_")[1].split(".")[0]
		global s
		s = GetValue()
		s.zpMass = int(mass)
		return s

def getLheList():
	for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
		s = store_ZpMass(name)
	    	try:
	    	    with open(name) as f: # No need to specify 'r': this is the default.
	    	    	for lheFile in f:
						if lheFile.find(Str) > 0:
							weightValue = lheFile.split(' : ')[1]
							s.weight = weightValue
							lheWeightList.append(s)
	    	except IOError as exc:
	    	    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
	    	        raise # Propagate other kinds of IOError.
	return lheWeightList


def main():
	List = getLheList()
	print 'ZpMass:',List[0].zpMass," Xsec:",List[0].weight
	# print a[2].weight

if __name__ == "__main__":
   main()
