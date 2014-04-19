libnatasha
==========

Natasha - Network Able to Transmit Amid Severly Hostile Activity 


Installation Instructions
=======================

download libsodium and install according to instructions

Install the following packages:
- python-dev
- python-pip
- libffi-dev

Then run:
```
sudo pip install pynacl
sudo easy-install GitPython
```


Add the following to your path:

```
export PATH=$PATH:/path/to/libnatasha
```

Finally, copy settings.conf.sample to settings.conf and change the settings to match your node's deployment schema


Manual Configuration Steps
========================

on host:
```
rsync -avz nodeX-deploy node-address.local:~/
```

on node (as root):
```
echo nodeX > /etc/hostname
nano /etc/hosts
```
replace 
```127.0.1.1       raspberrypi```
with
```127.0.1.1       nodeX```

Reboot. After reboot:

```
mv ~/nodeX-deploy ~/plp
sudo cp ~/libnatasha/install/gollum-server /etc/init.d/
sudo chmod 755 /etc/init.d/gollum-server
cp ~/libnatasha/install/config.rb ~/plp/config.rb
sudo update-rc.d gollum-server defaults

```
