#!/bin/bash
scriptname=`basename $0`
EXPECTED_ARGS=2
if [ $# -ne $EXPECTED_ARGS ]
then
echo "Usage: $scriptname workdirectory rootFileIndex"
echo "Example: ./$scriptname $PWD 1"
exit 1
fi

if [ ! -e $1/step1.py ]; then
 echo $1/"step1.py does not exist!"
exit 1
fi


cd $1

export SCRAM_ARCH=slc6_amd64_gcc481; eval `scramv1 runtime -sh`
filein=step0_MZp1000_MChi1000_$2_numEvent1000.root
echo "input file is" $filein
if [ ! -e $1/$filein ]; then
 echo $1/$filein " does not exist!"
exit 1
fi
fileout=MZp1000_MChi1000/step1/step1_MZp1000_MChi1000_$2.root
echo "output file is" $fileout
rm -rf $fileout
cmsRun step1.py inputFiles=file:$filein outputFile=$fileout
