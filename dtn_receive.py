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
import pickle, os, dtn

def main():
  # generate keys
  if dtn.keyCheck('node1') == False and dtn.keyCheck('node2') == False:
    dtn.keyMake('node1')
    dtn.keyMake('node2')

  inputFile = raw_input('enter the name of the payload file: ')
  with open(inputFile, 'r') as payloadFile:
    output = pickle.load(payloadFile)
    
  print type(output)
  print dtn.openPayload(output)
  return 0

if __name__ == '__main__':
	main()

