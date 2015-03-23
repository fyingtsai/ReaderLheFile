#!/usr/bin/python2.7
# Author: Kelly Tsai

import sys
import glob
import errno

class GetValue():
    def __init__(self):
    	self.fileName = ''
    	self.weight = []
    	self.tanBeta = []

lheList = []
Str = 'Integrated weight (pb)'
path = '/Users/KellyTsai/Documents/MadGraph/Zp_hA0_bb_hleFile/*.lhe'   
files = glob.glob(path) 

def getLheList():
	for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
	    try:
	        with open(name) as f: # No need to specify 'r': this is the default.
	        	for lheFile in f:
					if lheFile.find(Str) > 0:
						s = GetValue()
						weightValue = lheFile.split(' : ')[1]
						s.weight = weightValue
						lheList.append(s)
	    except IOError as exc:
	        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
	            raise # Propagate other kinds of IOError.
	return lheList
def main():
	a = getLheList()
	# print a[2].weight
	print a.weight

if __name__ == "__main__":
   main()
