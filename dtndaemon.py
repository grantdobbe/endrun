#!/usr/bin/env python

import dtn
import threading
import sys
import os
import time

logfile = '/var/log/dtn_transfer.log'
incoming_pipe = '/tmp/received'

if len(sys.argv) != 2:
  print "usage: python serialdaemon.py /path/to/serial"
  exit()

logout = open(logfile, 'a')

def logthis(data):
  logout.write("["+time.ctime()+"] " + data + "\n");
  logout.flush()

def processBundle(filename):
  logthis("Opened file " + filename +  " for processing by Natasha.")  
  dtn.receive(filename)

def listen():
  with open(incoming_pipe, 'r') as received:
    while 1:
      incoming = received.readlines()
      
      if len(incoming) > 0:
        filename = incoming
        if ".data" in filename:
          processBundle(filename)
      else:
        time.sleep(1)

logthis("Starting up.")

listenthread = threading.Thread(target=listen)
listenthread.daemon = True
listenthread.start()

