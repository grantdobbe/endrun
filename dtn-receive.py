#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dtn-receive.py
#  
#  Copyright 2013 Grant Dobbe <grant@dobbe.us>
#  

import dtn, sys

def main():
  
  if len(sys.argv) != 2:
    print "usage: python dtn-receive.py payload"
    exit()
    
  payload = sys.argv[1]
  
  dtn.receive(payload)
	
if __name__ == '__main__':
	main()

