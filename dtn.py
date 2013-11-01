#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
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

#import pynacl
import time, base64, os, nacl.utils
from nacl.public import PrivateKey, Box

class Payload:
  # time-to-live - unix timestamp of now + 24 hours 
  ttl = int(time.time()+86400)
  # source - a hash of the source's public key
  # TODO: figure this out more later
  source = "me"
  # destination - a hash of the source's private key
  # TODO: figure this out more later
  destination = "you"
  # nonce = a number used once for purposes of encryption and decryption
  # TODO: research better methods of generating nonces
  nonce = nacl.utils.random(Box.NONCE_SIZE)
  # payload - nacl encrypted bzipped tarball 
  # empty by default
  payload = ""
  
  # encrypt a tarball and save it to the payload
  # args:
  def serialize():
    # use pynacl for this
 
    
  def deserialize():
    # use pynacl for this
    
    
  # grab a git bundle from a repo and create a payload
  # args: 
  #   repo: the fully qualified path to a git repo
  #   destination: the public key of the delivery target for the payload
  # returns: 
  #   a payload for delivery
  def pack(repo, destination):
    # change to the git repo's directory
    # if there is no $NODE-current branch, create $NODE-current wherever HEAD is
    # create a git bundle from master
    #   if $NODE-current == HEAD, do everything from the first commit
    #   otherwise, do everything from $NODE-current to HEAD
    #     then, once we have successfully created a bundle, delete the $NODE-current tag and reassign it to HEAD
    # tar and bzip the bundle
    # encrypt the tarball using the destination's public key (call serialize() )
    # run it through base64 and pipe it into self.payload
    # clean up after ourselves (delete the .bundle file and the encrypted tarball)
    # export the entire payload with headers into a file
    
  # import a payload, decrypt the git payload inside, and perform a git pull
  def unpack(repo, source):
    # decrypt the tarball using our private key (call deserialize() )
    # untar and decompress the bundle
    # if a remote for the source doesn't exist in our repo, create one
    # otherwise, copy the bundle file to the destination specified in our .git/config file
    # change to the git repo's directory
    # run a verify against the bundle
    # if we are missing the necessary commits, die and say which ones
    # otherwise, do a git pull from the bundle file
    # clean up after ourselves (delete the encrypted payload and the tarball)
    
    
  

def main():
	return 0

if __name__ == '__main__':
	main()

