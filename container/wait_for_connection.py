#!/usr/bin/env python

import sys
import socket
import time
import os

if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    service_is_alive = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tries = 0
    print("Waiting on connection to start...")
    while not service_is_alive and tries < 100:
        tries += 1
        try:
            print("Checking host %s:%s" % (host, port))
            s.connect((host, port))
        except socket.error:
            time.sleep(3)
        else:
            service_is_alive = True

    if service_is_alive:
        print("Service started!")
        sys.exit(0)
    else:
        print("Unable to reach %s on port %s" % (host, port))
sys.exit(1)
