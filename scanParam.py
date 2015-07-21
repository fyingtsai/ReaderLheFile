# Author: Kelly Tsai

import sys
import os
import glob
import fileinput
import subprocess

str_mzp = 'mzp'
str_pidzp = '50'
str_ma0 = 'ma0'
str_pida0 = '28'
str_mdm = 'mx'
str_pidx = '1000022'
fileName = 'param_card.dat'
paramCard = glob.glob(fileName)


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def replaceMZp(searchExp,replaceExp):
    for line in fileinput.input(fileName, inplace=1):
    	if line.lower().find(str_mzp)>0 and line.find(str_pidzp)>0:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def replaceMA0(searchExp,replaceExp):
    for line in fileinput.input(fileName, inplace=1):
    	if line.lower().find(str_ma0)>0 and line.find(str_pida0)>0:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def replaceMDM(searchExp,replaceExp):
    for line in fileinput.input(fileName, inplace=1):
    	if line.lower().find(str_mdm)>0 and line.find(str_pidx)>0:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def getHiggsAutoWidth():
    for line in fileinput.input(paramCard, inplace=1):
        line = line.strip('\r')
        if line.find("ECAY  25")>0:
            hWidth = line.split("25   ")[1].split(" #")[0]
            line = line.replace(hWidth,"Auto")
        sys.stdout.write(line)

def getA0AutoWidth():
    for line in fileinput.input(paramCard, inplace=1):
        #line = line.strip('\r')
        if line.find("ECAY  28")>0:
            A0Width = line.split("28   ")[1].split(" #")[0]
            line = line.replace(A0Width,"Auto")
        sys.stdout.write(line)

def getZpAutoWidth():
    for line in fileinput.input(paramCard, inplace=1):
        #line = line.strip('\r')
        if line.find("ECAY  50")>0:
            ZpWidth = line.split("50   ")[1].split(" #")[0]
            line = line.replace(ZpWidth,"Auto")
        sys.stdout.write(line)

def generateEvent():
    s = subprocess.Popen('./bin/generate_events -f', shell=True)
    s.wait()
    return s.returncode

#replaceMZp(sys.argv[1],sys.argv[2])
# replaceMZp('1.200000e+03','500')
#getA0AutoWidth()
#getZpAutoWidth()
#getHiggsAutoWidth()

def main():
    replaceMZp("1.000000e+03","6.000000e+02")
    with cd(".."):
        generateEvent()
    getHiggsAutoWidth()
    getZpAutoWidth()
    getA0AutoWidth()
    replaceMA0("3.000000e+02","400")
    with cd(".."):
        generateEvent()
    getHiggsAutoWidth()
    getZpAutoWidth()
    getA0AutoWidth()

if __name__ == "__main__":
   main()

