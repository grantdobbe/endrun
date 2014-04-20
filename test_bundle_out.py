#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_bundle_out.py
#  
#  Copyright 2014 Grant Dobbe <grant@dobbe.us>
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

def bundle_out(destination):
  dtn.pack(destination)

def main():
  if len(sys.argv) != 2:
    print "usage: python test_bundle_out.py destination"
    exit()
  
  destination = sys.argv[1]
  
  bundle_out(destination)

if __name__ == '__main__':
	main()

