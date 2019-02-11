#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "Specify target host and experiment name"
    exit 1
fi

LOGDIR=data/$2
mkdir -p $LOGDIR
iperf -c $1 -p 5001 -t 20 -i 0.5 -Z reno | tee $LOGDIR/iperf_${1}.txt
