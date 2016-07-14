#! /usr/bin/env python
#-------------------------------------------------------------
# File: scanParam.py
# Created: 14 July 2016 Fang-Ying Tsai
#------------------------------------------------------------- 

import glob
import errno
from ROOT import TGraph, TFile, TCanvas, TH2F, gStyle
from ROOT import TGraph2D
from array import array

class GetValue():
    def __init__(self):
    	self.fileNum = []
    	self.zpMass = []
    	self.ma0Mass = []
    	self.mdmMass = []
    	self.weight = []
    	self.tanbeta = []

hAList = []
hzList = []
  
hA_files = glob.glob(hApath) 


def getFile(fileName):
		num = str(fileName).split("_")[1].split(".")[0]
		global s
		s = GetValue()
		s.fileNum = int(num)
		return s

def getMZpValue(readLine):
	mzpValue = float(readLine.strip().split(' # ')[0].split('32 ')[1])
	return mzpValue

def getMA0Value(readLine):
	ma0Value = float(readLine.strip().split(' # ')[0].split('28 ')[1])
	return ma0Value

def getMDMValue(readLine):
	mdmValue = float(readLine.strip().split(' # ')[0].split('1000022 ')[1])
	return mdmValue

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
	    	    		if lheFile.find('mzp') > 0:
	    	    			s.zpMass = getMZpValue(lheFile)
	    	    		elif lheFile.find('ma0') > 0:
	    	    			s.ma0Mass = getMA0Value(lheFile)
	    	    		elif lheFile.find('mx') > 0:
	    	    			s.mdmMass = getMDMValue(lheFile)
	    	    		elif lheFile.find('Integrated weight') > 0:
	    	    			s.weight = getWeightValue(lheFile)
	    	    		elif lheFile.find('tb') > 0 and lheFile.find('#') > 0:
	    	    			s.tanbeta = getTanBeta(lheFile)
					hAList.append(s)
	    	except IOError as exc:
	    	    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
	    	        raise # Propagate other kinds of IOError.
	return hAList

def main():
	f = TFile("ScanPlot_fixgz.root","recreate")
	c1 = TCanvas( 'c1', 'A Simple Graph', 200, 10, 700, 500 )
	c1.SetGrid()

	hAList = gethAList(hA_files)

	histo_hA02 = TH2F('xsec2','Xsec(Zp>h(bb)+A0(2DM),gz=0.8), dm = 100GeV', 22, 500,2600,8,200,900)
	histo_hA02.SetXTitle("M_Zp (GeV)")
	histo_hA02.SetYTitle("M_A0 (GeV)")
	histo_hA02.SetStats(0)

	for a in hAList:
		histo_hA02.Fill(a.zpMass,a.ma0Mass, (a.weight))
	gStyle.SetPalette(1)

	f.Write()
	f.Close()
	c1.Update()

if __name__ == "__main__":
   main()
