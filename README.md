libnatasha
==========

Natasha - Network Able to Transmit Amid Severly Hostile Activity 

Manual Configuration Steps
=================

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
sudo cp ~/libnatasha/gollum-server /etc/init.d/
sudo chmod 755 /etc/init.d/gollum-server
cp ~/libnatasha/config.rb ~/plp/config.rb
sudo update-rc.d gollum-server defaults

```
