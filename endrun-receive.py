#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  endrun-receive.py
#  
#  Copyright 2013 Grant Dobbe <grant@dobbe.us>
#  

import endrun, sys

def main():
  
  if len(sys.argv) != 2:
    print "usage: python endrun-receive.py payload"
    exit()
    
  payload = sys.argv[1]
  
  endrun.receive(payload)
	
if __name__ == '__main__':
  main()

