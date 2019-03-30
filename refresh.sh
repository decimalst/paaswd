#!/bin/bash

#deletes any python in the home folder and copies new stuff from mac folder mount	
rm ~/*.py
rm ~/sql/*.sql

cp /vagrant/*.py ~/.
cp /vagrant/sql/*.sql ~/sql/