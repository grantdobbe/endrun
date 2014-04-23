#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  serialdaemon.py
#  
#  Copyright 2013 Brendan O'Connor <ussjoin@ussjoin.com>
#  

import serial
import threading
import sys
import os
import errno
import time

incoming_pipe_name = '/tmp/tobesent'
outgoing_pipe_name = '/tmp/received'

logfile = '/var/log/plp_serial.log'
plp_incoming_dir = '/tmp/plp_incoming'

outgoing_data_global = []

if len(sys.argv) != 2:
  print "usage: python serialdaemon.py /path/to/serial"
  exit()

if not os.path.exists(incoming_pipe_name):
  os.mkfifo(incoming_pipe_name)

if not os.path.exists(outgoing_pipe_name):
  os.mkfifo(outgoing_pipe_name)

if not os.path.exists(plp_incoming_dir):
  os.makedirs(plp_incoming_dir)

pipeinfd = os.open(incoming_pipe_name, os.O_RDONLY | os.O_NONBLOCK)
pipeout = open(outgoing_pipe_name, 'w+')

logout = open(logfile, 'a')

ser = serial.Serial(sys.argv[1], 19200, timeout=1)

def logthis(data):
  logout.write("["+time.ctime()+"] "+data+"\n");
  logout.flush()

def handleincomingdata(data):
  #print data
  logthis("Received "+str(sum(len(s) for s in data))+" bytes.")
  
  randomname = 'incoming-'+str(time.time())+'.data'

  outfile = open(plp_incoming_dir+'/'+randomname, 'w')

  for ditem in data:
    outfile.write(ditem)
  
  outfile.close()

  pipeout.write(plp_incoming_dir+'/'+randomname+"\n")
  pipeout.flush() # Write it out RIGHT NOW.
  # But you could do anything else you wanted here.

def listen():
  while 1:
    incoming = ser.readlines()
    if len(incoming) > 0:
      handleincomingdata(incoming)
    else:
      time.sleep(1)

def speak(data):
  ser.write(data)
  logthis("Shipped out "+str(len(data))+" bytes.")

def wait_to_speak():
  while True:
    if len(outgoing_data_global) > 0:
      data = outgoing_data_global.pop(0) #Take front thing off list
      speak(data)
    else:
      time.sleep(1)

logthis("Starting up.")

listenthread = threading.Thread(target=listen)
listenthread.daemon = True
listenthread.start()

speakthread = threading.Thread(target=wait_to_speak)
speakthread.daemon = True
speakthread.start()

while 1:
  try:
    d = os.read(pipeinfd, 1024*10)
  except OSError as err:
    if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
      d = None
      # This is a fine condition; just means nothing this cycle
    else:
      raise

  if (d is not None and len(d) >= 1):
    #print d
    logthis("Queuing for send "+str(len(d))+" bytes now.")
    outgoing_data_global.append(d)
  else:
    time.sleep(1)
    

