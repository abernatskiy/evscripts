#!/bin/bash

# Usage: ./movie.sh <forceGain> <sensorGain> <network>

# On most monitors, you will need to modity Bullet's
# source code to get this running. Change line 81 of
# Demos/OpenGL/GlutStuff.cpp to take 0s instead of
# width/2, height/2, then cd to build3/gmake
# (assuming you use bullet3) and rebuild the library

if [ $# -lt 7 ]; then
	echo Not enough arguments
	exit 1
elif [ $# -gt 7 ]; then
	echo Too many arguments
	exit 1
fi

source vars

CLIENT_MAIN=$CLIENT_DIR/tadrosim-graphics

CURDIR="`pwd`"
CLIENT_MAKE_LOG=$CURDIR/client_make.log
CLIENT_LOG=$CURDIR/client.log

function spawnGraphicalClient(){
	# Spawns a client process. Arguments:
  # $1    compilation options
	# $2    remake/noremake
  cd "$CLIENT_DIR"
  make clean > "$CLIENT_MAKE_LOG" 2>&1
  make tadrosim-graphics MORECFLAGS="$1" >> "$CLIENT_MAKE_LOG" 2>&1
	echo making tadrosim-graphics MORECFLAGS="$1" ...
#  make tadrosim-graphics MORECFLAGS="$1"
	./tadrosim-graphics in out > "$CLIENT_LOG" &
#	./tadrosim-graphics in out &
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
echo sending `echo $@ | cut -d' ' -f3-` to in
echo $@ | cut -d' ' -f3- > $CLIENT_DIR/in
sleep 1
CLIENT_WINDOWID=`wmctrl -l | grep "Bullet Physics Demo. http:\/\/bulletphysics.com" | cut -d' ' -f1`
recordmydesktop --windowid $CLIENT_WINDOWID --no-sound --overwrite -o fg${1}sg${2}nw`echo $@ | cut -d' ' -f4- | sed -e 's/ //g'`.ogv &
RMD_PID=$!

cat $CLIENT_DIR/out &
echo CRASHLANDING > $CLIENT_DIR/in &

waitForPID $CLIENT_PID

kill $RMD_PID
