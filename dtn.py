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
import time, os, pickle, ConfigParser, git, shutil
import nacl.utils, nacl.encoding, nacl.signing
from nacl.public import PrivateKey, Box

NONCE_SIZE = 24

'''
Grab the config file (we're gonna need it later on)
'''
config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '/settings.conf')


'''
-----------------
Class declaration
-----------------
'''
class Payload:
  
  ttl = config.get('global', 'ttl')
  # origin - a unique identifier that can be used to pull up my public key
  origin = config.get('global', 'nodename')
  # destination - a unique identifier that can be used to pull up their private key
  destination = ''
  # nonce = a number used once for purposes of encryption and decryption
  nonce = nacl.utils.random(NONCE_SIZE)
  # payload - nacl encrypted git bundle 
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
  #   contents: binary data to be encrypted and assigned to the payload object
  def wrap(self, payload_contents ):
    # look up the signature key
    with open( config.get('global', 'keypath') + '/' + self.origin + '.sig', 'r') as originSigKey:
      originSig = self.deserialize(originSigKey)
    # look up the public and private keys
    with open( config.get('global', 'keypath') + '/' + self.origin + '.private', 'r' ) as originPrivateKey:
      originKey = self.deserialize(originPrivateKey)
    with open( config.get('global', 'keypath') + '/' + self.destination + '.public', 'r' ) as destinationPublicKey:
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
    with open( config.get('global', 'keypath') + '/' + self.destination + '.private', 'r' ) as destinationPrivateKey:
      destinationKey = self.deserialize(destinationPrivateKey)
    # grab the origin's public key
    with open( config.get('global', 'keypath') + '/' + self.origin + '.public', 'r' ) as originPublicKey:
      originKey = self.deserialize(originPublicKey)
    # grab the origin's verification key
    with open( config.get('global', 'keypath') + '/' + self.origin + '.sighex', 'r' ) as originSigHex:
      originSigKey = self.deserialize(originSigHex)
      originVerify = nacl.signing.VerifyKey(originSigKey, encoder=nacl.encoding.HexEncoder)
    # create a box to decrypt this sucker
    container = Box(destinationKey, originKey)
    # verify the signature
    rawResult = originVerify.verify(self.payload)
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
  def pack(self, destination):
    self.destination = destination
    # change to the git repo's directory
    repo = git.Repo(config.get('global', 'repopath'))
    # if there is no $NODE-current branch, create $NODE-current wherever HEAD is
    repo.git.checkout(B=self.origin)
    repo.git.merge('master')
    # create a git bundle from master
    bundleName = self.origin + '.bundle'
    repo.git.bundle('create', '/tmp/' + bundleName, self.origin)
    # encrypt the tarball using the destination's public key (call serialize() )
    with open('/tmp/' + bundleName, 'r') as payloadInput:
       self.wrap(payloadInput.read())
    # export the entire payload with headers into a file
    with open('/tmp/' + bundleName + '.dtn', 'w') as payloadFile:
      pickle.dump(bundleName, payloadFile)
    # clean up after ourselves (delete the .bundle file)
    #os.remove('/tmp/' + bundleName)
    # import a payload, decrypt the git payload inside, and perform a git pull
    return 0
  
  def unpack(self):
    repo = git.Repo(config.get('global', 'repo'))
    bundlePath = config.get('global', 'bundlepath')
    trackingBranch = self.origin + '-remote/' + self.origin
    bundleName = self.origin + '.bundle'
    # decrypt the bundle using our private key 
    payload = bytes(self.unwrap())
    # save the bundle file in /tmp/

    with open('/tmp/' +  bundleName, 'wb') as bundleFile:
      bundleFile.write(payload)
    # run a verify against the bundle
    print repo.git.bundle('verify', bundlePath + '/' + bundleName)
    # copy the bundle file to the destination specified in our .git/config file
    copyfile('/tmp/' + bundleName, bundlePath + '/' + bundleName)
    # do a git pull from the bundle file
    repo.git.checkout(trackingBranch)
    repo.git.pull()
    repo.git.checkout('master')
    repo.git.merge(trackingBranch)
    repo.git.gc()
    repo.git.checkout(trackingBranch)
    repo.git.merge('master')
    repo.git.checkout('master')
    # clean up after ourselves (delete the encrypted payload and the tarball)
    os.remove('/tmp/' + bundleName)
    return 0
'''
---------------
Helper Functions
---------------
'''  

'''
crypto initialization and checks
'''
def keyCheck(node):
  # check for a valid key pair and return true if found, false otherwise    
  result = False
  if os.path.exists(config.get('global', 'keypath') + '/' + node + '.public') and os.path.exists(config.get('global', 'keypath') + '/' + node + '.private') and os.path.exists(node + '.sig') and os.path.exists(node + '.sighex'):
    result = True
  return result
  
def keyMake(node):
  ## create a public, private, and signature key set
  # generate the encryption keypair
  key = PrivateKey.generate()
  # generate the signature key
  sig = nacl.signing.SigningKey.generate()
  verify = sig.verify_key
  sig_hex = verify.encode(encoder=nacl.encoding.HexEncoder)
  
  # write all of the keys to file
  with open(config.get('global', 'keypath') + '/' + node + '.sig', 'w+') as signing_key:
    pickle.dump(config.get('global', 'keypath') + '/' + sig, signing_key) 
  with open(config.get('global', 'keypath') + '/' + node + '.sighex', 'w+') as verify_hex:
    pickle.dump(sig_hex, verify_hex)
  with open(config.get('global', 'keypath') + '/' + node + '.private', 'w+') as private:
    pickle.dump(key, private)
  with open(config.get('global', 'keypath') + '/' + node + '.public', 'w+') as public:
    pickle.dump(key.public_key, public)

'''
Node setup and configuration
'''
# generate the DTN keys we need for each node
def generateKeys(nodeTotal, path):
  nodes = []
  keyPath = path + "/keys"
  
  # if the directory doesn't exist, create it
  if not os.path.exists(keyPath):
    os.makedirs(keyPath)
  # switch to that directory
  os.chdir(keyPath)
  print 'Generating keys: ',
  # create one key set for each node
  for node in range (1, nodeTotal + 1):
    nodeName = 'node' + str(node)
    keyMake(nodeName)
    print("."),
  
  # print a progress message for the user
  print "\nKey generation complete."

# generate an empty repo with the correct number of branches for each node
def repoInit(nodeTotal, path):
  # set up the actual deployment path
  deployPath = path + '/repo'
  
  # create the directory if it's not there yet
  if not os.path.exists(deployPath):
    os.makedirs(deployPath)
  
  print "Creating repo and branches: ",
  # init an empty repo
  repo = git.Repo.init(deployPath)
  
  # write a file so that we have something to move around
  filetext = "This is created during node configuration. Add any additional instructions here."
  readmeName = deployPath + '/README.md'
  with open(readmeName, 'w+') as readme:
    readme.write(filetext)

  # commit said file  
  repo.git.add(readmeName)
  repo.git.commit(m='initial commit to repo')
  
  # create a branch for each node we need to work with
  for node in range(1, nodeTotal + 1):
    nodeName = 'node' +  str(node)
    repo.git.checkout(b=nodeName)
    print '.',
  # checkout the master branch again
  repo.git.checkout('master')

  # print a progress message for the user
  print "\nMaster repo creation complete."

# create the node-specific config directories and run the "round robin"
def nodeInit(nodeTotal, path):
  
  print "Creating node deployment files: ",
  # define the parent repo
  parentRepo = path + '/repo'
  # define the parent key directory
  parentKeys = path + '/keys'
  # define the parent bundle path
  parentBundles = path + '/bundles'
  if not os.path.exists(parentBundles):
    os.makedirs(parentBundles)

  # set up the deploy directory and set up everything except bundles
  for node in range(1, nodeTotal + 1):
    # define some variables we'll need
    nodeName = "node" + str(node)
    nodePath = path + '/' + nodeName + '-deploy'
    repoPath = nodePath + '/repo'
    keyPath = nodePath + '/keys'
    bundlePath = nodePath + '/bundles'
    # create a directory named nodeX-deploy for each node
    if not os.path.exists(nodePath):
      os.makedirs(nodePath)
    # create a directory called repo
    if not os.path.exists(repoPath):
      os.makedirs(repoPath)    
    # clone the repo in that directory
    repo = git.Repo.clone_from(parentRepo, repoPath)
    # create a bundle of this repo and drop it in the parent folder
    repo.git.checkout(b=nodeName)
    repo.git.bundle('create', parentBundles + '/' + nodeName + ".bundle", nodeName)
    repo.create_tag('bundle-' + nodeName + '-0')
    # create a directory called bundles (leave it empty for now)
    if not os.path.exists(bundlePath):
      os.makedirs(bundlePath)
    # create a directory called keys
    if not os.path.exists(keyPath):
      os.makedirs(keyPath)
    # copy in:
    #  this node's private crypto key
    shutil.copy(parentKeys + '/' + nodeName + '.private', keyPath)
    #  this node's private sig key
    shutil.copy(parentKeys + '/' + nodeName + '.sig', keyPath)
    for files in os.listdir(parentKeys):
      #  everyone's public crypto key
      if files.endswith(".public"):
        shutil.copy(parentKeys + '/' + files, keyPath)
      #  everyone's public sig key
      if files.endswith(".sighex"):
        shutil.copy(parentKeys + '/' + files, keyPath)
    print '.',
  print "\nRepos cloned, keys copied, and bundles created."

  # now create the bundles and set them up in each repo 
  print "Adding bundles as remote repos and creating tracking branches: ",
  for node in range(1, nodeTotal + 1):
    # define some variables we'll needcd ..
    nodeName = "node" + str(node)
    nodePath = path + '/' + nodeName + '-deploy'
    repoPath = nodePath + '/repo'
    bundlePath = nodePath + '/bundles'  
    repo = git.Repo(repoPath)
    # copy every bundle except yourself
    for files in os.listdir(parentBundles):
      if not files.startswith(nodeName):
        shutil.copy(parentBundles + '/' + files, bundlePath)
    # add a remote for every bundle you have
    for files in os.listdir(bundlePath):
      remoteName = files.split('.')
      remote = repo.create_remote(remoteName[0] + '-remote', bundlePath + '/' + files)
      remote.fetch()
      trackingBranch = remoteName[0] + '-remote/' + remoteName[0]
      repo.git.checkout(b=trackingBranch)
    repo.git.checkout('master')
    print '.',
  print "\nProcess complete."
    
  print str(nodeTotal) + " nodes ready for deployment."

'''
Payload functions
'''
# create a payload for the user 
def createPayload(destination, data):
  payload = Payload()
  payload.pack(destination)
  
# open a payload for the user
def openPayload(payload):
  with open(payload, 'r') as payloadFile:
    raw_payload = pickle.load(payloadFile) 
    raw_payload.unpack()

