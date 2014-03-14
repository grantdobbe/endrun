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

import os, dtn

	
	
def main():
	home = os.path.expanduser("~") + "/plp-test"
	
	number = int(raw_input("Enter the number of nodes to create (default is 5): ") or 5 ) 
	path = raw_input("Define the output path for the files and repos (no trailing slash, default is ~/plp-test): ") or home
	
	dtn.generateKeys(number, path)
	dtn.repoInit(number, path)
	return 0

if __name__ == '__main__':
	main()

