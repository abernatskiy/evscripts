#!/bin/bash

source vars

CLIENT_MAIN=$TADROSIM_DIR/tadrosim

EVS_MAIN=$EVS_DIR/main.py
EVS_PIPE_INDIV=$EVS_DIR/individuals.pipe
EVS_PIPE_EVALS=$EVS_DIR/evaluations.pipe
EVS_RESULTS=$EVS_DIR/bestIndividual.log

CURDIR="`pwd`"

EVS_LOG=$CURDIR/evs.log
CLIENT_LOG=$CURDIR/client.log
CLIENT_MAKE_LOG=$CURDIR/client_make.log
RESULTS=$CURDIR/rawResults.ssv

CAT_TIMEOUT=0.1s

function safeCat(){
	timeout $CAT_TIMEOUT cat "$1"
}

function cleanPipes(){
  safeCat $EVS_PIPE_INDIV > /dev/null
  safeCat $EVS_PIPE_EVALS > /dev/null
}

function spawnClient(){
	# Spawns a client process. Arguments:
  # $1    compilation options
	# $2    remake/noremake
  cd "$CLIENT_DIR"
  make clean > "$CLIENT_MAKE_LOG" 2>&1
  make tadrosim MORECFLAGS="$1" >> "$CLIENT_MAKE_LOG" 2>&1
	./tadrosim "$EVS_PIPE_INDIV" "$EVS_PIPE_EVALS" > "$CLIENT_LOG" &
	CLIENT_PID=$!
	cd "$CURDIR"
#	echo Spawned a client process, PID $CLIENT_PID
}

function spawnEVS(){
	# Spawns an EVS process. Arguments: none
	cd "$EVS_DIR"
	./main.py "$1" > "$EVS_LOG" &
	EVS_PID=$!
	cd "$CURDIR"
#	echo Spawned a server process, PID $EVS_PID
}

function checkPIDExistence(){
	kill -0 $1 > /dev/null 2>&1
}

function waitForPID(){
	while (checkPIDExistence $1); do
		sleep 0.1
	done
}

echo -n "force_gain: ${1} sensor_gain: ${2}" >> $RESULTS
spawnClient "-DFORCE_GAIN=${1}f -DSENSOR_GAIN=${2}f"
for i in 7881 1543 106 4899 8591 6604 4356 4775 7870 7317; do
	spawnEVS $i
	waitForPID $EVS_PID
	echo -n " " >> $RESULTS
	echo -n seed${i}: `tail -1 "$EVS_RESULTS" | cut -d " " -f 2-` >> $RESULTS
done
kill $CLIENT_PID
echo >> $RESULTS
