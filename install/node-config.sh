#!/bin/bash


NODE=$1
SRC=$2

HOSTNAME=$(hostname)

echo "updating libnatasha repo"
cd /home/$USER/libnatasha 
git pull origin master

cd /home/$USER/

echo "copying in repo installation files"
rsync -a $SRC/$NODE-deploy $HOME/
mv $HOME/$NODE-deploy $HOME/plp

echo "changing host-specific settings"
sudo sed -i "s/$HOSTNAME/$NODE/g" /etc/hostname
sudo sed -i "s/127\.0\.1\.1	$HOSTNAME/127\.0\.1\.1	$NODE/g" /etc/hosts
sudo cp /home/$USER/libnatasha/install/gollum-server /etc/init.d/
sudo chmod 755 /etc/init.d/gollum-server
cp $HOME/libnatasha/install/config.rb $HOME/plp/config.rb
sudo update-rc.d gollum-server defaults

echo "installing serial daemon"
sudo cp ~/libnatasha/install/natasha-serial /etc/init.d/
sudo update-rc.d natasha-serial defaults

echo "changing bundle paths"
sed -i "s;/home/gdobbe/plp-test/$NODE-deploy;$HOME/plp;g" $HOME/plp/repo/.git/config

echo "all done!"
