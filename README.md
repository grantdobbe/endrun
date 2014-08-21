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
sudo cp ~/libnatasha/install/natasha-serial /etc/init.d/
sudo update-rc.d natasha-serial defaults
sudo cp ~/libnatasha/install/hostapd /etc/init.d/
sudo cp ~/libnatasha/install/dnsmasq.conf /etc/
```

Generate your certificate and key. (Add script to make this easier later.) Then:

```
cat the.pem the.key > server.pem
sudo cp server.pem /etc/lighttpd/server.pem
sudo cp /etc/lighttpd/lighttpd.conf /etc/lighttpd/lighttpd.conf.old
sudo cp ~/libnatasha/install/lighttpd.conf /etc/lighttpd/lighttpd.conf
sudo /etc/init.d/lighttpd restart
```
