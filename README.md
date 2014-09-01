Endrun
==========

Endrun is a project for secure digital communication without the internet. It can be used to create a 
disruption-tolerant, delay-tolerant, opsec-friendly communications network where data can be moved by
any means available.


Installation Steps
=======================

download libsodium and install according to instructions

Install the following packages:
- python-dev
- python-pip
- libffi-dev

Then run:
``` 
sudo pip install pynacl
sudo easy_install GitPython
``` 


Add the following to your path:

```
export PATH=$PATH:/path/to/endrun
```

Finally, copy settings.conf.sample to settings.conf and change the settings to match your node's deployment schema

Automatic Node Configuration
=========================

on host:
```
rsync -avz endrun-deploy node-address.local:~/
```

on node (as root):
apt-get install git
apt-get install sudo

git clone git@github.com:grantdobbe/endrun.git


Manual Configuration Steps
========================

on host:
```
rsync -avz endrun-deploy node-address.local:~/
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
sudo cp ~/endrun/install/gollum-server /etc/init.d/
sudo chmod 755 /etc/init.d/gollum-server
cp ~/endrun/install/config.rb ~/plp/config.rb
sudo update-rc.d gollum-server defaults
sudo cp ~/endrun/install/endrun-daemon /etc/init.d/
sudo update-rc.d endrun-daemon defaults
sudo cp ~/endrun/install/hostapd /etc/init.d/
sudo cp ~/endrun/install/dnsmasq.conf /etc/
```

Generate your certificate and key. (Add script to make this easier later.) Then:

```
cat the.pem the.key > server.pem
sudo cp server.pem /etc/lighttpd/server.pem
sudo cp /etc/lighttpd/lighttpd.conf /etc/lighttpd/lighttpd.conf.old
sudo cp ~/endrun/install/lighttpd.conf /etc/lighttpd/lighttpd.conf
sudo /etc/init.d/lighttpd restart
```
