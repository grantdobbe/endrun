#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dtn_test1.py
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
    print "usage: python dtn_transmit.py source-node destination-node payloadfile"
    exit()
    
  # get nodes from command line path
  source = sys.argv[1]
  destination = sys.argv[2]
  # get bundle file from command line path

  #data = raw_input('Enter some text: ')
  data = sys.argv[3]
  
  print 'making a payload and saving it to file'
  output = dtn.createPayload('node1', 'node2', data)
  
  with open(str(fileinput.filename() + '.dtn', 'w+') as payloadFile:
    pickle.dump(output, payloadFile)
  return 0

if __name__ == '__main__':
	main()

