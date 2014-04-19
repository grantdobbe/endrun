#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dtn_test2.py
#  
#  Copyright 2013 Grant Dobbe <grant@binarysprocket.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import pickle, os, dtn, sys

def main():
  
  if len(sys.argv) != 2:
    print "usage: python dtn_receive.py payloadfile"
    exit()
    
  filename = sys.argv[1]
  with open(filename, 'r') as payloadFile:
    output = pickle.load(payloadFile)
    bundle = bytes(dtn.openPayload(output))
    
  with open(filename[:-4], 'wb') as bundleFile:
    bundleFile.write(bundle)
    
  return 0

if __name__ == '__main__':
	main()

