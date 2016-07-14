#! /bin/bash

for((i=1;i<6;i++))
do
  cd Events/run_0$i
  gunzip unweighted_events.lhe.gz 
  mv unweighted_events.lhe gz05.lhe
  cp gz05.lhe ../../LHEfile
done