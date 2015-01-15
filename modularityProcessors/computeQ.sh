#!/bin/bash

CURDIR=`pwd`

WORKDIR="/home/iriomotejin/findcommunities/"
QCOMPUTER="${WORKDIR}massQ.sh"

cd $WORKDIR

for file in ${CURDIR}/bestIndividual*.log; do
	cat $file | tail -n +2 | cut -d ' ' -f3- | head -50 | $QCOMPUTER > ${file}.q
done

cd $CURDIR
