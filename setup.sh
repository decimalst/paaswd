#!/bin/bash

#depends on usage of vagrant - needs to be expanded for other VM/provisioning	
cp /vagrant/*.py /home/vagrant/

if [ ! -f my_file ]; 	
then 
	touch my_file
fi

if [ ! -f home/vagrant/test.db ]; 	
then 
	sqlite3 /home/vagrant/test.db < /vagrant/TABLE_USER_PASSWD.sql
fi
