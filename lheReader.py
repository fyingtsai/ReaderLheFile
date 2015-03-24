# Author: Kelly Tsai
import glob
import errno
from ROOT import TGraph, TFile, TCanvas
from array import array

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

def getWeightValue(readLine):
	weightValue = float(readLine.split(' : ')[1])
	return weightValue	 

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
	    	    			s.weight = getWeightValue(lheFile)
					lheWeightList.append(s)
	    	except IOError as exc:
	    	    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
	    	        raise # Propagate other kinds of IOError.
	return lheWeightList

def main():
	f = TFile("lhe.root","recreate")
	c1 = TCanvas( 'c1', 'A Simple Graph', 200, 10, 700, 500 )
	c1.SetGrid()
	xMass = []
	yWeight = []
	yTanBeta = []
	List = getLheList()
	for m in List:
		xMass.append(m.zpMass)
		yWeight.append(m.weight)
		yTanBeta.append(m.mh_2/m.mh)
	x = array("d", xMass)
	y = array("d", yWeight)
	y1 = array("d",yTanBeta)
	g = TGraph(len(x),x,y)
	g2 = TGraph(len(x),x,y1)
	g.GetXaxis().SetTitle("ZpMass (GeV)")
	g.GetYaxis().SetTitle("Weight (Pb)")
	g.SetMarkerColor(4)
	g.SetMarkerStyle(21)
	g.Write('AP')
	g2.GetXaxis().SetTitle("ZpMass (GeV)")
	g2.GetYaxis().SetTitle("tan(beta) (mh_2/mh)")
	g2.SetMarkerColor(4)
	g2.SetMarkerStyle(21)
	g2.Write('AP')
	# f.Write()
	f.Close()
	c1.Update()
	# print List[2].mh_2/List[2].mh
if __name__ == "__main__":
   main()
