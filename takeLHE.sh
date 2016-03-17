#! /bin/bash
massPoint=(600 800 1000 1200 1400 1700 2000 2500)
for mass in ${massPoint[@]}; 
do
    cmsRun dumpLHE_cfg.py inputFiles="file:/afs/cern.ch/work/f/fatsai/CMSSW_7_1_14/src/gridpack/LHEFile/cmsgrid_final_${mass}.lhe" outputFile="RootFile/output_${mass}.root" maxEvents=-1

done
