#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dtn-transmit.py
#  
#  Copyright 2013 Grant Dobbe <grant@dobbe.us>
#  

import dtn, sys

def main():
  if len(sys.argv) != 2:
    print "usage: python dtn-transmit.py destination"
    exit()
  
  destination = sys.argv[1]
  
  transmit(destination)

if __name__ == '__main__':
	main()
