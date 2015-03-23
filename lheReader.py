# Author: Kelly Tsai

import sys
import glob
import errno

class GetValue():
    def __init__(self):
    	self.zpMass = []
    	self.weight = []
    	self.mh_2 = []
    	self.mh = []

lheWeightList = []
lheZpMassList = []
str_weight = 'Integrated weight (pb)'
str_Mh = 'Mh'
str_mh__2 = 'mh__2'
path = '/Users/KellyTsai/Documents/MadGraph/Zp_hA0_bb_hleFile/*.lhe'   
files = glob.glob(path) 

def store_ZpMass(fileName):
		mass = str(fileName).split("events_")[1].split(".")[0]
		global s
		s = GetValue()
		s.zpMass = int(mass)
		return s

def getMhValue(readLine):
	mhValue = float(readLine.split(' # ')[0].split()[1])
	return mhValue

def getmh_2Value(readLine):
	mh__2Value = float(readLine.split(' # ')[0].split()[1])
	return mh__2Value

def getLheList():
	for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
		s = store_ZpMass(name)
	    	try:
	    	    with open(name) as f: # No need to specify 'r': this is the default.
	    	    	for lheFile in f:
	    	    		if lheFile.find(str_mh__2) > 0:
	    	    			s.mh_2 = getmh_2Value(lheFile)
	    	    		elif lheFile.find(str_Mh) > 0:
	    	    			s.mh = getMhValue(lheFile)
	    	    		elif lheFile.find(str_weight) > 0:
						weightValue = lheFile.split(' : ')[1]
						s.weight = weightValue
						lheWeightList.append(s)
	    	except IOError as exc:
	    	    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
	    	        raise # Propagate other kinds of IOError.
	return lheWeightList


def main():
	List = getLheList()
	print List[2].mh_2/List[2].mh

if __name__ == "__main__":
   main()
