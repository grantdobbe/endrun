#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setup.py
#  
#  Copyright 2014 Grant Dobbe <grant@binarysprocket.com>
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

import pickle, os, time
from dtn import keyMake

def generateKeys():
	nodes = []
	nodeTotal = int(raw_input("Enter the number of nodes to create: "))
	
	if not os.path.exists('keys'):
		os.makedirs('keys')
	
	os.chdir('keys')
	
	start = time.clock()
	for node in range (1, nodeTotal + 1):
		nodeName = 'node' + str(node)
		keyMake(nodeName)
	end = time.clock()
	
	difference = end - start
	print 
	print "Setup complete. Generated " + str(nodeTotal) + " keys in " + str(difference) + " seconds."
	print "Keys can be found in ./keys."

def main():
	generateKeys()
	return 0

if __name__ == '__main__':
	main()

