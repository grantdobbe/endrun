#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cell_create.py
#  
#  Copyright 2014 Grant Dobbe <grant@dobbe.us>
#    

import os, endrun, time, sys
  
def main():
  
  if len(sys.argv) != 3:
    
    # grab the user's home directory
    path = os.path.expanduser("~") + "/endrun-deploy"
  
    # fetch our intial config data
    number = int(raw_input("Enter the number of nodes to create (default is 8): ") or 8 )
    prefix = raw_input("What naming prefix should we use for nodes? (default is node): ") or "node"
    
    start = time.time()
    
    # generate the keys
    endrun.generateKeys(number, path, prefix)
    # create the repo
    endrun.repoInit(number, path, prefix)
    # create a directory for each node following the convention prefixX-deploy with the appropriate info
    endrun.nodeInit(number, path, prefix)
    
    end = time.time()
    
    # figure out how long it took
    difference = end - start
    
    # tell the user we're done
    print "Node configuration complete. " + str(number) + " nodes created in " + str(difference) + " seconds."
    print "Output can be found in " + path + "."
    print "Copy these files prior to generating another Endrun cell."
    return 0

if __name__ == '__main__':
  main()

