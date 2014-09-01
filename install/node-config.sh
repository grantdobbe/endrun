#!/bin/bash


NODE=$1
SRC=$2

HOSTNAME=$(hostname)

if [ -z $1 -o -z $2] 
  then
    echo "USE: node-config.sh nodename /path/containing/node-deploy"
    exit
fi

echo "updating endrun repo"
cd /home/$USER/endrun 
git pull origin master

cd /home/$USER/

echo "copying in repo installation files"
rsync -a $SRC/$NODE-deploy $HOME/
mv $HOME/$NODE-deploy $HOME/endrun-data

echo "creating a config file"
cp $HOME/endrun/settings.conf.sample $HOME/endrun/settings.conf
sed -i "s/nodeX/$NODE/g" $HOME/endrun/settings.conf

echo "adding ~/endrun to your path"
echo "export PATH=$PATH:$HOME/endrun" >> $HOME/.bashrc

echo "changing host-specific settings"
sudo sed -i "s/$HOSTNAME/$NODE/g" /etc/hostname
sudo sed -i "s/127\.0\.1\.1	$HOSTNAME/127\.0\.1\.1	$NODE/g" /etc/hosts
sudo cp /home/$USER/endrun/install/gollum-server /etc/init.d/
sudo sed -i "s;/home/pi/endrun-data/repo;$HOME/endrun-data/repo;g" /etc/init.d/gollum-server
sudo chmod 755 /etc/init.d/gollum-server
cp $HOME/endrun/install/config.rb $HOME/endrun-data/config.rb
sed -i "s/nodeX/$NODE/g" $HOME/endrun-data/config.rb

sudo update-rc.d gollum-server defaults
sudo cp $HOME/endrun/install/hostapd /etc/init.d/

#echo "installing serial daemon"
#sudo cp $HOME/endrun/endrun-daemon /etc/init.d/
#sudo update-rc.d endrun-daemon default

echo "changing bundle paths"
sed -i "s;/home/(.*)/endrun-deploy/$NODE-deploy;$HOME/endrun-data;g" $HOME/endrun-data/repo/.git/config

echo "all done!"
