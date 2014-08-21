#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  endrun-transmit.py
#  
#  Copyright 2013 Grant Dobbe <grant@dobbe.us>
#  

import endrun, sys

def main():
  if len(sys.argv) != 2:
    print "usage: python endrun-transmit.py destination"
    exit()
  
  destination = sys.argv[1]
  
  endrun.transmit(destination)

if __name__ == '__main__':
	main()
