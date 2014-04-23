#!/bin/bash


NODE=$1
SRC=$2

HOSTNAME=$(hostname)

if [ -z $1 ] 
  then
    echo "USE: node-config.sh nodename /path/containing/node-deploy"
    exit
fi

if [ -z $2 ] 
  then
    echo "USE: node-config.sh nodename /path/containing/node-deploy"
    exit
fi

echo "updating libnatasha repo"
cd /home/$USER/libnatasha 
git pull origin master

cd /home/$USER/

echo "copying in repo installation files"
rsync -a $SRC/$NODE-deploy $HOME/
mv $HOME/$NODE-deploy $HOME/plp

echo "adding ~/libnatasha to your path"
echo "export PATH=$PATH:$HOME/libnatasha" >> $HOME/.bashrc

echo "changing host-specific settings"
sudo sed -i "s/$HOSTNAME/$NODE/g" /etc/hostname
sudo sed -i "s/127\.0\.1\.1	$HOSTNAME/127\.0\.1\.1	$NODE/g" /etc/hosts
sudo cp /home/$USER/libnatasha/install/gollum-server /etc/init.d/
sudo chmod 755 /etc/init.d/gollum-server
cp $HOME/libnatasha/install/config.rb $HOME/plp/config.rb
sudo update-rc.d gollum-server defaults
sudo cp $HOME/libnatasha/install/hostapd /etc/init.d/

echo "installing serial daemon"
sudo cp $HOME/libnatasha/install/natasha-serial /etc/init.d/
sudo update-rc.d natasha-serial defaults

echo "changing bundle paths"
sed -i "s;/home/gdobbe/plp-test/$NODE-deploy;$HOME/plp;g" $HOME/plp/repo/.git/config

echo "all done!"
