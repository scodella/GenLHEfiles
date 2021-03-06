#!/bin/bash

FILEDIR=$1
PROCNAME=$2
DECAYNAME=$3
CFGNAME=$4

# grid proxy check
voms-proxy-info --all > /dev/null
if [ $? -ne 0 ]; then
  voms-proxy-init -voms cms --valid 168:00
fi

for FILEPATH in `ls /eos/uscms/store/user/pedrok/${FILEDIR}/${PROCNAME}*`
  do
    FILE=`basename ${FILEPATH}`
    xrdcp root://cmseos.fnal.gov//store/user/pedrok/${FILEDIR}/${FILE} lhe/
  done

# add some command line options?
python update_header.py ${CFGNAME} --stableLSP

for FILEPATH in `ls lhe_processed/${DECAYNAME}*`
  do
    FILE=`basename ${FILEPATH}`
    xrdcp ${FILEPATH} root://cmseos.fnal.gov//store/user/pedrok/${FILEDIR}/${FILE}
  done
