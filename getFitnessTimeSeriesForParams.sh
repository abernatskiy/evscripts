#!/bin/bash

# Usage: getFitnessTimeSeriesForParams.sh forceGain sensorGain connectionCost randomSeedsFileName

source evscripts-funcs

CURFILENAME="./fg${1}sg${2}cc${3}_fitnessTimeSeries.dat"
echo "# Fitness time series are based on random seeds from ${4}" > $CURFILENAME

spawnClient "-DFORCE_GAIN=${1}f -DSENSOR_GAIN=${2}f -DCONNECTION_COST=${3}f"

IFS=$'\n'
for rseed in `cat ${4}`; do
	spawnEVS $rseed
	waitForPID $EVS_PID
	cat "$EVS_RESULTS" | awk '{print $2}' | tail -n +2 | tr '\n' ' ' >> $CURFILENAME
	echo >> $CURFILENAME
done

kill $CLIENT_PID
