# paaswd

## Requirements
- Virtualbox (if running from Mac/Windows)
- Vagrant (Or some other way to bring up a basic linux server, with python3 and pip installed)
- Python3
- pip
- flask
- pytest

## How this works:

Paaswd gives read-only access to a linux system's /etc/passwd file.

It consists of two scripts, one which watches the /etc/passwd file for changes and writes changes to a sqlite database, and a Flask-based webapp which allows queries to the underlying database.

## Setup

### If using Vagrant:
1. Clone the repository.
2. Run the vagrant file with "vagrant up" - This should run the provisioning steps in the vagrant file.
3. ssh into the machine, and run the /opt/paaswd/watch_dog.py as a user with access to the /etc/paaswd and /etc/group files, that can write to /tmp/ via python3 watch_dog.py
4. Start the flask app with sh run.sh
5. Access the app via localhost:8080/ and localhost:8080/api/

### If installing on a bare VM:
1. Place all repo files in a directory /opt/paaswd/ on a server, which is not externally facing.
2. Install python3 and pip.
3. Install the module by going to /opt/paaswd/paaswd-app/ and running 'pip install .'
4. Run the passwd file watch script /opt/paaswd/watch_dog.py as a user with access to the /etc/paaswd and /etc/group files, that can write to /tmp/ via python3 watch_dog.py. watch_dog.py has command line arguments to point at different files if desired.
5. Modify run.sh to have host=127.0.0.1 as the argument to "flask run", then run it with 'sh run.sh'
6. Access the app at localhost:5000/ and localhost:5000/api/


## Design justification:

Basically, I didn't want to have a webservice directly access /etc/passwd/.
The watchdog process should have read-write access to the sqlite database, and privileges to look at /etc/passwd, but the flask webapp would technically need read-only access to the sqlite database. This setup at least adds a buffer where if the webapp is broken for remote code execution, an attacker also needs to find a privilege escalation exploit on the system.


## To-do

1. Add swagger docs to the API - This is at the top of the to-do list.
2. Better flesh out the pytests of the flask app. Currently they hit all of the API endpoints, but could go more in-depth.
3. Better mapping for the responses from the API - currently they're just raw json.