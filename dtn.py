#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dtn.py
#  
#  Copyright 2013 Grant Dobbe <grant@dobbe.us>
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
import time, os, pickle, ConfigParser
import nacl.utils, nacl.encoding, nacl.signing
from nacl.public import PrivateKey, Box

NONCE_SIZE = 24

class Payload:
  
  ttl = int(time.time()+86400)
  # origin - a unique identifier that can be used to pull up my public key
  origin = ''
  # destination - a unique identifier that can be used to pull up their private key
  destination = ''
  # nonce = a number used once for purposes of encryption and decryption
  nonce = nacl.utils.random(NONCE_SIZE)
  # payload - nacl encrypted bzipped tarball 
  # empty by default
  payload = ''
  
  # serializes whatever is fed to it
  def serialize(self, material):
    return pickle.dump(material)
    
  #deserializes whatever is fed to it
  def deserialize(self, material):
    return pickle.load(material)
  
  # encrypts data and saves it to the payload
  # args:
  #   origin: a string representing the origin node's unique identifier
  #   destination: a string representing the destination node's unique identifier
  #   contents: binary data to be encrypted and assigned to the payload object
  def wrap(self, origin, destination, payload_contents ):
    # address the payload
    self.origin = origin
    self.destination = destination
    # look up the signature key
    with open( origin + '.sig', 'r') as originSigKey:
      originSig = self.deserialize(originSigKey)
    # look up the public and private keys
    with open( origin + '.private', 'r' ) as originPrivateKey:
      originKey = self.deserialize(originPrivateKey)
    with open( destination + '.public', 'r' ) as destinationPublicKey:
      destinationKey = self.deserialize(destinationPublicKey)
    # make payload a NaCL box
    container = Box( originKey, destinationKey )
    # sign the contents
    signedContents = originSig.sign(payload_contents)
    # encrypt the payload
    rawPayload = container.encrypt( signedContents, self.nonce )
    # sign the payload and attach it to the object
    self.payload = originSig.sign( rawPayload )
    
  # decrypt a payload and return the contents
  # args:
  #   none
  # return:
  #   a decrypted tarball containing a git bundle or False otherwise
  def unwrap(self):
    # grab my private key
    with open( self.destination + '.private', 'r' ) as destinationPrivateKey:
      destinationKey = self.deserialize(destinationPrivateKey)
    # grab the origin's public key
    with open( self.origin + '.public', 'r' ) as originPublicKey:
      originKey = self.deserialize(originPublicKey)
    # grab the origin's verification key
    with open( self.origin + '.sighex', 'r' ) as originSigHex:
      originSigKey = self.deserialize(originSigHex)
      originVerify = nacl.signing.VerifyKey(originSigKey, encoder=nacl.encoding.HexEncoder)
    
    # create a box to decrypt this sucker
    container = Box(destinationKey, originKey)
    # verify the signature
   # rawResult = originVerify.verify(self.payload)
    rawResult = self.payload
    # decrypt it
    rawResult = container.decrypt(rawResult)
    # verify the signature again
    result = originVerify.verify(rawResult)
    return result
            
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
    return 0
  
  def unpack(self, repo, source):
    # decrypt the tarball using our private key (call deserialize() )
    # untar and decompress the bundle
    # if a remote for the source doesn't exist in our repo, create one
    # otherwise, copy the bundle file to the destination specified in our .git/config file
    # change to the git repo's directory
    # run a verify against the bundle
    # if we are missing the necessary commits, die and say which ones
    # otherwise, do a git pull from the bundle file
    # clean up after ourselves (delete the encrypted payload and the tarball)
    return 0
  
    
def keyCheck(node):
  # check for a valid key pair and return true if found, false otherwise    
  result = False
  if os.path.exists(node + '.public') and os.path.exists(node + '.private') and os.path.exists(node + '.sig') and os.path.exists(node + '.sighex'):
    result = True
  return result
  
def keyMake(node):
  # create a public, private, and signature key set

  # generate the encryption keypair
  key = PrivateKey.generate()
  # generate the signature key
  sig = nacl.signing.SigningKey.generate()
  
  verify = sig.verify_key
  sig_hex = verify.encode(encoder=nacl.encoding.HexEncoder)
  
  with open(node + '.sig', 'w+') as signing_key:
    pickle.dump(sig, signing_key) 
  with open(node + '.sighex', 'w+') as verify_hex:
    pickle.dump(sig_hex, verify_hex)
  with open(node + '.private', 'w+') as private:
    pickle.dump(key, private)
  with open(node + '.public', 'w+') as public:
    pickle.dump(key.public_key, public)
    
def createPayload(source, destination, message):
  payload = Payload()
  payload.wrap(source, destination, message)
  return payload
  
def openPayload(payload):
  return payload.unwrap()

