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
import pickle, os
from nacl.public import PrivateKey, Box
from dtn import Payload

def keyCheck(node):
  result = False
  if os.path.exists(node + '.public') and os.path.exists(node + '.private'):
    result = True
  return result

def keyMake(node):
  key = PrivateKey.generate()
  with open(node + '.private', 'w+') as private:
    pickle.dump(key, private)
  with open(node + '.public', 'w+') as public:
    pickle.dump(key.public_key, public)

def createPayload(source, destination, message):
  payload = Payload()
  payload.serialize(source, destination, message)
  return payload
  
def openPayload(payload):
  return payload.deserialize()

def main():
  # generate keys
  if keyCheck('node1') == False and keyCheck('node2') == False:
    keyMake('node1')
    keyMake('node2')

  inputFile = raw_input('enter the name of the payload file: ')
  with open(inputFile, 'r') as payloadFile:
    output = pickle.load(payloadFile)
    
  print type(output)
  print openPayload(output)
  return 0

if __name__ == '__main__':
	main()

