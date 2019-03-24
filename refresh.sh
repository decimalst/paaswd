#!/bin/bash

#deletes any python in the home folder and copies new stuff from mac folder mount	
rm ~/*.py

cp /vagrant/*.py ~/.
