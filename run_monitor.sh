#!/bin/bash

if [[ $UID -ne 0 ]]; then 
    echo "Run with sudo"
    exit 1
fi

if [[ $# -ne 1 ]]; then
    echo "Specify experiment name"
    exit 1
fi

LOGDIR=data/$1
mkdir -p $LOGDIR

rmmod tcp_probe > /dev/null 2>&1
modprobe tcp_probe port=5001
cat /proc/net/tcpprobe | tee $LOGDIR/tcpprobe.txt
