#!/usr/bin/python3

from argparse import ArgumentParser
import os
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

"""Extracts CWND and SSTHRESH values from a file containing output from 
tcpprobe; datapath is a directory that contains a file called 'tcpprobe.txt';
lines that do not contain the dst_filter in the destination column should be 
ignored; returns three lists containing timestamps (float), cwnd (int), and 
ssthresh (int) values"""
def parse_data(datapath, dst_filter='5001'):
    filepath = os.path.join(datapath, 'tcpprobe.txt')

    # TODO

    return [], [], []

def sanitize_data(time, cwnd, ssthresh):
    time = [t - time[0] for t in time]
    return time, cwnd, ssthresh

"""Create a plot of cwnd and ssthresh over time; the plot should be a png file 
called tcpvars.png saved in the datapath directory"""
def plot_data(datapath, time, cwnd, ssthresh):
    filepath = os.path.join(datapath, 'tcpvars.png')
    plt.figure(1, figsize=(10, 5))

    # TODO

    plt.savefig(filepath)

def main():
    # Parse arguments
    arg_parser = ArgumentParser(description='Summarize latency')
    arg_parser.add_argument('-d', '--datapath', dest='datapath', action='store',
            required=True, help='Path to directory of data')
    settings = arg_parser.parse_args()

    time, cwnd, ssthresh = parse_data(settings.datapath)
    time, cwnd, ssthresh = sanitize_data(time, cwnd, ssthresh)
    plot_data(settings.datapath, time, cwnd, ssthresh)

if __name__ == '__main__':
    main()
