#!/bin/bash

source vars

CLIENT_MAIN=$CLIENT_DIR/tadrosim-graphics
CLIENT_MAKE_LOG="client_make.log"
CLIENT_LOG="client.log"

CURDIR="`pwd`"

function spawnGraphicalClient(){
	# Spawns a client process. Arguments:
  # $1    compilation options
	# $2    remake/noremake
  cd "$CLIENT_DIR"
  make clean > "$CLIENT_MAKE_LOG" 2>&1
  make tadrosim-graphics MORECFLAGS="$1" >> "$CLIENT_MAKE_LOG" 2>&1
	./tadrosim-graphics in out > "$CLIENT_LOG" &
	CLIENT_PID=$!
	cd "$CURDIR"
#	echo Spawned a client process, PID $CLIENT_PID
}

function checkPIDExistence(){
	kill -0 $1 > /dev/null 2>&1
}

function waitForPID(){
	while (checkPIDExistence $1); do
		sleep 0.1
	done
}

spawnGraphicalClient "-DFORCE_GAIN=${1}f -DSENSOR_GAIN=${2}f"
echo $@ | cut -d' ' -f3- > $CLIENT_DIR/in

cat $CLIENT_DIR/out
kill $CLIENT_PID
