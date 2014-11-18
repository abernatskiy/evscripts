#!/bin/bash

source evscripts-funcs

CURFILENAME="./fg${1}sg${2}_timeSeries.dat"

spawnClient "-DFORCE_GAIN=${1}f -DSENSOR_GAIN=${2}f"
spawnEVS ${3}
waitForPID $EVS_PID

cat "$EVS_RESULTS" | awk '{print $2}' | tail -n +2 | tr '\n' ' ' >> $CURFILENAME

kill $CLIENT_PID
echo >> $CURFILENAME
