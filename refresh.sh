#!/bin/bash
#deletes any python in the paaswd folder and copies new stuff from host folder mount	
rm /opt/paaswd/*.sh
rm /opt/paaswd/*.py
rm /opt/paaswd/sql/*
rm -rf /opt/paaswd/paaswd-app/

cp /vagrant/*.sh /opt/paaswd/
cp /vagrant/*.py /opt/paaswd/
cp /vagrant/sql/* /opt/paaswd/sql/
cp -r /vagrant/paaswd-app /opt/paaswd/