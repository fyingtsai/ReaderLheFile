# Author: Kelly Tsai
import glob
import errno
from ROOT import TGraph, TFile, TCanvas
from array import array

class GetValue():
    def __init__(self):
    	self.fileNum = []
    	self.zpMass = []
    	self.weight = []
    	self.tanbeta = []

hAList = []
hzList = []
str_weight = 'Integrated weight'
str_tanBeta = 'tb'
str_tanBeta2 = '#'
str_MZp = 'mzp'
hApath = 'hA_*.lhe'
hzpath = 'hz_*.lhe'  
hA_files = glob.glob(hApath) 
hz_files = glob.glob(hzpath)

def getFile(fileName):
		num = str(fileName).split("_")[1].split(".")[0]
		global s
		s = GetValue()
		s.fileNum = int(num)
		return s

def getMZpValue(readLine):
	mzpValue = float(readLine.strip().split(' # ')[0].split('50')[1])
	return mzpValue

def getWeightValue(readLine):
	weightValue = float(readLine.split(' : ')[1])
	return weightValue	

def getTanBeta(readLine):
	tbValue  = float(readLine.split(' # ')[0].split()[1])
	return tbValue 

def gethAList(lhefile):
	for name in lhefile: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
		s = getFile(name)
	    	try:
	    	    with open(name) as f: # No need to specify 'r': this is the default.
	    	    	for lheFile in f:
	    	    		if lheFile.find(str_MZp) > 0:
	    	    			s.zpMass = getMZpValue(lheFile)
	    	    		elif lheFile.find(str_weight) > 0:
	    	    			s.weight = getWeightValue(lheFile)
	    	    		elif lheFile.find(str_tanBeta) > 0 and lheFile.find(str_tanBeta2) > 0:
	    	    			s.tanbeta = getTanBeta(lheFile)
					hAList.append(s)
	    	except IOError as exc:
	    	    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
	    	        raise # Propagate other kinds of IOError.
	return hAList

def gethzList(lhefile):
	for name in lhefile: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
		s1 = getFile(name)
	    	try:
	    	    with open(name) as f: # No need to specify 'r': this is the default.
	    	    	for lheFile in f:
	    	    		if lheFile.find(str_MZp) > 0:
	    	    			s1.zpMass = getMZpValue(lheFile)
	    	    		elif lheFile.find(str_weight) > 0:
	    	    			s1.weight = getWeightValue(lheFile)
	    	    		elif lheFile.find(str_tanBeta) > 0 and lheFile.find(str_tanBeta2) > 0:
	    	    			s1.tanbeta = getTanBeta(lheFile)
					hzList.append(s1)
	    	except IOError as exc:
	    	    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
	    	        raise # Propagate other kinds of IOError.
	return hzList

def main():
	f = TFile("lhe.root","recreate")
	c1 = TCanvas( 'c1', 'A Simple Graph', 200, 10, 700, 500 )
	c1.SetGrid()

	Weight = []
	TanBeta_hz = []
	TanBeta_hA = []

	hAList = gethAList(hA_files)
	hzList = gethzList(hz_files)

	for i in range(0,4):
		Weight.append(((hAList[i].weight + hzList[i].weight)*1000)/0.57)
		TanBeta_hA.append(hAList[i].tanbeta)
		
	x = array("d", TanBeta_hA)
	y = array("d", Weight)

	g = TGraph(len(x),x,y)
	g.GetXaxis().SetTitle("tan(beta)")
	g.GetYaxis().SetTitle("Weight (fb)")
	g.SetMarkerColor(4)
	g.SetMarkerStyle(21)
	g.SetTitle("MZp = 1000 (GeV)")
	g.Write('AP')
	f.Write()
	f.Close()
	c1.Update()

if __name__ == "__main__":
   main()
