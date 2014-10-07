#!/bin/bash

EVS_DIR=$HOME/evs
TADROSIM_DIR=$HOME/bullet3-Bullet-2.83-alpha/Demos/Box2dDemo

EVS_MAIN=$EVS_DIR/main.py
TADROSIM_MAIN=$TADROSIM_DIR/tadrosim
TADROSIM_GRAPHICS=$TADROSIM_DIR/tadrosim-graphics

#CURDIR = ???

function runEvolution(){
  # Runs robotic evolution ONCE. Arguments:
  # $1    additional compilation options string
  cd "$TADROSIM_DIR";
  make clean;
}


echo $EVS_MAIN $TADROSIM_MAIN $TADROSIM_GRAPHICS
