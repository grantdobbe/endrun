#!/bin/bash


NODE=$1
SRC=$2

cd /home/$USER/libnatasha 
git pull origin master

cd /home/$USER/

rsync -av $SRC/$NODE-deploy /home/$USER/plp

sudo echo nodeX > /etc/hostname
sudo sed -i "s/127.0.1.1 raspberrypi/127.0.1.1 $NODE/g" /etc/hosts
sudo cp /home/$USER/libnatasha/install/gollum-server /etc/init.d/
sudo chmod 755 /etc/init.d/gollum-server
cp /home/$USER/libnatasha/install/config.rb /home/$USER/plp/config.rb
sudo update-rc.d gollum-server defaults

sed -i "s/\/home\/gdobbe\/plp-test\/node1-deploy/\/home\/$USER\/plp/g" /home/$USER/plp/repo/.git/config
