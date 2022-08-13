#!/usr/bin/env python3

import socket as s
import threading as th
import sys
import queue
import time

#        if code == 0 :
#            r_code = code
#        s.close()
# s.connect_ex((host, port))
try:
    target = sys.argv[1]
except:
    target = "localhost"
try:
    threads = int(sys.argv[2])
except:
    threads = 9

def udp_scan(target, port):
    r_code = 0
    sk = s.socket(s.AF_INET, s.SOCK_DGRAM)
    try:
        sk.settimeout(.1)
        s.sendto(b'test', (ip, port))
        data, addr = s.recvfrom(1024)
        return 1
    except Exception as e:
        if e is KeyboardInterrupt:
            sys.exit(1)
        return 0

def tcp_scan(target, port):
    sk = s.socket(s.AF_INET, s.SOCK_STREAM)
    try:
        # s.settimeout(1)
        sk.settimeout(.1)
        sk.connect((target, port))
        return 1
    except Exception as e:
        if e is KeyboardInterrupt:
            sys.exit(1)
        else:
            return 0


def printServiceOnPort(portNumber, protocol):
    try:
        serviceName = s.getservbyport(portNumber, protocol)
        print(f"{serviceName} on {portNumber}, {protocol}")
    except Exception as e:
        if e is KeyboardInterrupt:
            sys.exit(1)
        print(f"Unkown on {portNumber}, {protocol}")


def print_port(port):
	sys.stdout.flush()
	sys.stdout.write(f"{port}\r")



def get_ports():
        ports = queue.Queue()
        for port in range(65535):
            ports.put(port)
        #print(ports)
        return ports



def scan(target, port):
        #print(port)
        tcp = tcp_scan(target, port)
        udp = 0
        if tcp == 0:
            udp = udp_scan(target, port)
        if udp == 0:
            None
        if tcp == 1:
            printServiceOnPort(port, 'tcp')
        if udp == 1:
            printServiceOnPort(port, 'udp')


def start(target, ports):
      while not ports.empty():
            scan(target, ports.get())
#            time.sleep(.1)

ports = get_ports()
print(ports.get())
for thread in range(threads):
      t = th.Thread(target=start,args=(target, ports,))
      t.start()
