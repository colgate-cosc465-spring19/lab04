#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.cli import CLI

from argparse import ArgumentParser
from subprocess import Popen

class BottleneckTopo(Topo):
    def __init__(self, nodes=1, bandwidth=None, delay=None, loss=None, 
		queue=None):
        super(BottleneckTopo, self).__init__()

        # Create switches and inter-switch link
        self.addSwitch('s0', fail_mode='standalone')
        self.addSwitch('s1', fail_mode='standalone')
        if delay is not None:
            delay = '%dms' % delay
        self.addLink('s0', 's1', bw=bandwidth, delay=delay, loss=loss,
		max_queue_size=queue)

        # Create hosts and links
        for i in xrange(1, nodes*2+1):
            hostname = 'h%d' % i
            self.addHost(hostname)
            self.addLink(hostname, 's%d' % (i%2))
            
def main():
    # Parse arguments
    parser = ArgumentParser(description="Congestion control analysis network")
    parser.add_argument('--bandwidth', dest="bandwidth", type=int, 
            action="store", default=None, help="Bandwidth in Mbps")
    parser.add_argument('--delay', dest="delay", type=int, action="store",
            default=None, help="One-way delay in milliseconds")
    parser.add_argument('--loss', dest="loss", type=int, action="store",
            default=None, help="Loss percentage")
    parser.add_argument('--queue', dest="queue", type=int, action="store",
            default=None, help="Max queue size")
    parser.add_argument('--nodes', dest="nodes", type=int, action="store", 
            default=1, help="Number of nodes on each side of the bottleneck")
    args = parser.parse_args()

    if (args.queue is None and args.bandwidth is not None 
            and args.delay is not None):
        args.queue = (args.bandwidth / 8.0 * 2**20) * (args.delay/1000.0) / 1460
        if (args.queue < 4):
            args.queue = 4
        print "Setting queue to bandwidth x delay = %d" % args.queue

    # Configure system
    print "Configuring system..."
    Popen("sysctl -w net.ipv4.tcp_congestion_control=reno", shell=True).wait()
    Popen("sysctl -w net.ipv4.tcp_min_tso_segs=1", shell=True).wait()

    # Create topology
    print "Creating topology..."
    topo = BottleneckTopo(nodes=args.nodes, bandwidth=args.bandwidth, 
            delay=args.delay, loss=args.loss, queue=args.queue)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoPinCpus=True)
    
    # Start network
    print "Starting network..."
    net.start()

    # Start iperf
    for i in xrange(1, args.nodes+1):
        hostname = 'h%d' % (i*2)
        host = net.getNodeByName(hostname)
        host.cmd("iperf -s -w 16m -p 5001 -i 1 &")

    # Start command line interface
    CLI( net )    

    # Stop network
    print "Stopping network..."
    net.stop()
    Popen("killall -9 iperf", shell=True).wait()

if __name__ == '__main__':
    main()
