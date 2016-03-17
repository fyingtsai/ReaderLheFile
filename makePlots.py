#! /usr/bin/env python
#-------------------------------------------------------------
# File: makePlots.py
# Created: 16 March 2016 Kelly Tsai
#-------------------------------------------------------------  

import os,sys
from ROOT import *

def main():
    massPoints = [600, 800, 1000, 1200, 1400, 1700, 2000, 2500]
    for mass in massPoints:
        f1 = TFile("RootFile/output_"+str(mass)+".root")
        print 'test'
        h_scale = f1.Get("h_scale")
        h_pdf = f1.Get("h_pdf")

        c1 = TCanvas("c1","Example",800,400)
        c1.Divide(2)
        c1.cd(1)
        h_scale.Draw()
        
        c1.cd(2)
        h_pdf.Draw() 
        c1.SaveAs('RootFile/MZp'+str(mass)+'.png')
try:
    main()
except KeyboardInterrupt:
    print
    print "ciao!"
    print 
