#!/bin/bash

if [ ! -f /tmp/watch_dog_db.sqlite ]; 	
then 
	python3 /opt/paaswd/watch_dog.py --setup-db-only
fi