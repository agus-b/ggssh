#!/bin/bash
#
#  Author by Agus Bimantoro <agus.bimantoro@gdplabs.id>
#   
#  $install.sh - ggssh installation script
#
#

NAME=ggssh 
SOURCE_PATH=src
INSTALLATION_PATH=/usr/bin

# check if we're root
if [ "$(whoami)" != "root" ]; then
	echo "Error: you need to be root to install $NAME"
	exit 1
fi

# ask for confirmation
echo -n "Are you sure you want to install $NAME[y/n] "
read cek
if [ "$cek" != "y" -a "$cek" != "Y" ]; then
	echo "Cancel: Installation aborted."
	exit 1
fi

echo "Copying files..."
cp $SOURCE_PATH/ggssh.py $INSTALLATION_PATH/ggssh

echo "Setting executable flags..."
chmod 755 $INSTALLATION_PATH/ggssh


