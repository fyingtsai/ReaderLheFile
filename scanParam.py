#! /usr/bin/env python
#-------------------------------------------------------------
# File: scanParam.py
# Created: 12 July 2016 Fang-Ying Tsai
#-------------------------------------------------------------  

import sys
import os
import glob
import fileinput
import subprocess


fileName = 'param_card.dat'
paramCard = glob.glob(fileName)


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def replaceMZp(searchExp,replaceExp):
    for line in fileinput.input(fileName, inplace=1):
    	if line.lower().find('mzp')>0 and line.find('32')>0:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def replaceMA0(searchExp,replaceExp):
    for line in fileinput.input(fileName, inplace=1):
    	if line.lower().find('ma0')>0 and line.find('28')>0:
            line = line.replace(searchExp,replaceExp)
 	if line.lower().find("mh__2")>0 and line.find("26")>0:
	    line = line.replace(searchExp,replaceExp)
	if line.lower().find("mhp")>0 and line.find("27")>0:
	    line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def replaceMDM(searchExp,replaceExp):
    for line in fileinput.input(fileName, inplace=1):
    	if line.lower().find('mx')>0 and line.find('1000022')>0:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def getA0AutoWidth():
    for line in fileinput.input(paramCard, inplace=1):
        if line.find("ECAY  28")>0:
            A0Width = line.split("28 ")[1].split(" #")[0]
            line = line.replace(A0Width,"Auto")
        sys.stdout.write(line)

def getZpAutoWidth():
    for line in fileinput.input(paramCard, inplace=1):
        if line.find("ECAY  32")>0:
            ZpWidth = line.split("32 ")[1].split(" #")[0]
            line = line.replace(ZpWidth,"Auto")
        sys.stdout.write(line)

def gethAutoWidth():
    for line in fileinput.input(paramCard, inplace=1):
        if line.find("ECAY  25")>0:
            hWidth = line.split("25 ")[1].split(" #")[0]
            line = line.replace(hWidth,"Auto")
        sys.stdout.write(line)

def generateEvent():
    s = subprocess.Popen('./bin/generate_events -f', shell=True)
    s.wait()
    return s.returncode

def main():
    replaceMZp("1.000000e+03","6.000000e+02")
    with cd(".."):
        generateEvent()
    getZpAutoWidth()
    getA0AutoWidth()
    gethAutoWidth()
    replaceMA0("3.000000e+02","4.000000e+02")
    with cd(".."):
        generateEvent()
    getZpAutoWidth()
    getA0AutoWidth()
    gethAutoWidth()
    replaceMA0("4.000000e+02","5.000000e+02")
    with cd(".."):
        generateEvent()
    getZpAutoWidth()
    getA0AutoWidth()
    gethAutoWidth()
    replaceMA0("5.000000e+02","6.000000e+02")
    with cd(".."):
        generateEvent()


if __name__ == "__main__":
   main()

