#!/usr/bin/env python

import dtn
import threading
import sys
import os
import errno
import time

# specify log file and incoming pipe
logfile = '/var/log/dtn_transfer.log'
incoming_pipe = '/tmp/received'

# open the log file
logout = open(logfile, 'a')

# set up the pipe as a file descriptor with non-blocking I/O
pipeinfd = os.open(incoming_pipe, os.O_RDONLY | os.O_NONBLOCK)

# write stuff to log file
def logthis(data):
  logout.write("["+time.ctime()+"] " + data + "\n");
  logout.flush()

# the actual bundle processing
def processBundle(filename):
  logthis("Opened file " + filename +  " for processing by Natasha.")  
  try:
    dtn.receive(filename)
  except:
    logthis("Bundle processing for " + filename + " failed. Please check validity of file." )

# wait for stuff to come in    
def listen():
    while 1:
      try:
        incoming = os.read(pipeinfd, 1024*10)
        
        if len(incoming) > 0:
          filename = incoming.rstrip()
          if ".data" in filename:
            processBundle(filename)
          else:
            #print "Nothing coming in, boss"
            pass
        else:
          time.sleep(1)
          
      except OSError as err:
        if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
          incoming = None
          # This is a fine condition; just means nothing this cycle
        else:
          raise

logthis("Starting up.")

listenthread = threading.Thread(target=listen)
listenthread.daemon = True
listenthread.start()

while 1:
  time.sleep(1)

