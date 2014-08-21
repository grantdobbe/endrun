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
    home = os.path.expanduser("~") + "/endrun"
  
    # fetch our intial config data
    number = int(raw_input("Enter the number of nodes to create (default is 8): ") or 8 )
    path = raw_input("Define the output path for the files and repos (no trailing slash, default is ~/plp): ") or home
    
    start = time.time()
    
    # generate the keys
    endrun.generateKeys(number, path)
    # create the repo
    endrun.repoInit(number, path)
    # create a directory for each node following the convention nodeX-deploy with the appropriate info
    endrun.nodeInit(number, path)
    
    end = time.time()
    
    # figure out how long it took
    difference = end - start
    
    # tell the user we're done
    print "Node configuration complete. " + str(number) + " nodes created in " + str(difference) + " seconds."
    print "Output can be found in " + path + "."
  
    return 0

if __name__ == '__main__':
  main()

